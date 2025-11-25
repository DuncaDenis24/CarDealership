const express = require('express');
const axios = require('axios');
const cors = require('cors');
const mysql = require('mysql2/promise');

const app = express();
const PORT = 3001;

// Configuration
const OLLAMA_API = 'http://localhost:11434/v1/chat/completions';
const OLLAMA_MODEL = 'car-assistant'; // Using the fine-tuned car assistant model
const CAR_SERVICE_URL = 'http://localhost:8080';

// System prompt for AI filter extraction
const FILTER_EXTRACTION_PROMPT = `You are an intelligent car search assistant that understands natural language queries about cars.

AVAILABLE FIELDS:
- color: The color of the car (e.g., "black", "red", "blue")
- type: The type of car (must be one of: SEDAN, SUV, HATCHBACK, COUPE, CONVERTIBLE, WAGON, MINIVAN, PICKUP, SPORTS, LUXURY)
- model: The model of the car (e.g., "Camry", "Civic")
- priceRange: Use for terms like "cheap", "affordable", "budget", "expensive", "luxury"
- minPrice/maxPrice: Specific price range (use only if exact numbers are mentioned)
- minYear/maxYear: Manufacture year range
- isAutomatic: true/false for automatic transmission

CAR TYPE MAPPINGS (map these to the standard types above):
- Family car → SUV, MINIVAN, WAGON
- Sports car → COUPE, SPORTS, CONVERTIBLE
- City car → HATCHBACK, MINI
- Luxury car → LUXURY, SEDAN (high-end)
- Off-road → SUV, PICKUP
- Economy car → HATCHBACK, SEDAN (lower price)
- Electric/EV → (set type based on body style, e.g., SEDAN, SUV)

PRICE RANGES (use priceRange field for these terms):
- cheap/affordable/budget → "budget"
- mid-range → "midrange"
- expensive → "expensive"
- luxury → "luxury"
- premium → "premium"

RULES:
1. Extract ALL filters that are explicitly or implicitly mentioned
2. For color: use lowercase (e.g., "black" not "Black")
3. For type: use UPPERCASE from the standard types listed above
4. For price-related terms, use priceRange field instead of minPrice/maxPrice
5. Only include the JSON object in your response, nothing else
6. If no filters are mentioned, return an empty object {}

EXAMPLES:
Input: "I need a cheap family car"
Output: {"type": ["SUV", "MINIVAN"], "priceRange": "budget"}

Input: "show me fast sports cars"
Output: {"type": ["COUPE", "SPORTS"], "priceRange": "expensive"}

Input: "looking for an affordable sedan"
Output: {"type": "SEDAN", "priceRange": "budget"}

Input: "best luxury suv"
Output: {"type": "SUV", "priceRange": "luxury"}

Input: "mid-range hatchback"
Output: {"type": "HATCHBACK", "priceRange": "midrange"}

Input: "show me all cars"
Output: {}

Input: "what red cars do you have?"
Output: {"color": "red"}`;

// Database connection
const pool = mysql.createPool({
  host: 'localhost',
  user: 'root', // Try with root user or create a dedicated user
  password: '240703', // Your MySQL root password (if any)
  database: 'scd_db',
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
});

// Test database connection
async function testConnection() {
  try {
    const connection = await pool.getConnection();
    console.log('Successfully connected to MySQL database');
    connection.release();
    
    // Create tables if they don't exist
    await createTables();
  } catch (error) {
    console.error('Error connecting to MySQL:', error);
    process.exit(1);
  }
}

// Create necessary tables
async function createTables() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS chat_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        conversation_id VARCHAR(255) NOT NULL,
        user_message TEXT,
        ai_response TEXT,
        filters TEXT,
        results_count INT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )`);
    console.log('Database tables verified/created');
  } catch (error) {
    console.error('Error creating tables:', error);
  }
}

// Test the connection when starting up
testConnection();

// In-memory cache for learning
const conversationHistory = new Map();

app.use(cors());
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
    res.json({ status: 'ok', message: 'AI Service is running' });
});

// Proxy for car-related requests
app.use('/api/cars', async (req, res) => {
    try {
        const response = await axios({
            method: req.method,
            url: `${CAR_SERVICE_URL}/api/cars${req.url}`,
            headers: req.headers,
            data: req.body
        });
        res.json(response.data);
    } catch (error) {
        console.error('Error proxying car request:', error);
        res.status(error.response?.status || 500).json({
            error: 'Failed to fetch car data',
            details: error.message
        });
    }
});

// Chat endpoint with Ollama integration
// Generate AI response with car data
async function generateAIResponse(message, cars, conversation = []) {
    try {
        if (cars.length === 0) {
            return "No matching cars found. Try different criteria.";
        }

        // Count cars by type for quick stats
        const typeCounts = cars.reduce((acc, car) => {
            const type = car.type || 'Unknown';
            acc[type] = (acc[type] || 0) + 1;
            return acc;
        }, {});

        // Get price range
        const prices = cars.map(car => car.price || 0).filter(p => p > 0);
        const minPrice = prices.length ? `$${Math.min(...prices).toLocaleString()}` : '';
        const maxPrice = prices.length ? `$${Math.max(...prices).toLocaleString()}` : '';
        
        // Build simple response
        let response = `Found ${cars.length} cars`;
        
        // Add type distribution if not too many types
        const typeList = Object.entries(typeCounts).map(([type, count]) => `${count} ${type}`).join(', ');
        if (typeList) {
            response += ` (${typeList})`;
        }
        
        // Add price range if available
        if (minPrice && maxPrice) {
            response += `, from ${minPrice} to ${maxPrice}`;
        }
        
        return response + '.';
    } catch (error) {
        console.error('Error generating AI response:', error);
        return "I'm having trouble processing your request. Here are some vehicles that might interest you:";
    }
}

app.post('/api/chat', async (req, res) => {
    try {
        const { message, cars: initialCars, conversationId } = req.body;

        if (!message) {
            return res.status(400).json({ error: 'Message is required' });
        }

        console.log('Received chat request:', { message, hasInitialCars: !!initialCars, conversationId });

        // Get or create conversation history
        const conversation = conversationHistory.get(conversationId) || [];

        // Add user message to conversation history
        conversation.push({ role: 'user', content: message });

        try {
            // Get car data from database if not provided
            let carData = [];
            try {
                if (initialCars && Array.isArray(initialCars) && initialCars.length > 0) {
                    carData = initialCars;
                } else {
                    const [rows] = await pool.query('SELECT * FROM cars');
                    carData = rows.map(row => ({
                        ...row,
                        // Ensure all expected fields exist
                        make: row.make || '',
                        model: row.model || '',
                        type: (row.type || '').toLowerCase(),
                        color: (row.color || '').toLowerCase(),
                        price: Number(row.price) || 0,
                        dailyRate: Number(row.dailyRate) || 0,
                        year: Number(row.year) || 0,
                        transmission: (row.transmission || '').toLowerCase(),
                        features: Array.isArray(row.features) ? row.features : []
                    }));
                }
            } catch (dbError) {
                console.error('Error fetching car data:', dbError);
                return res.status(500).json({
                    role: 'assistant',
                    content: "I'm having trouble accessing the car database. Please try again later.",
                    error: process.env.NODE_ENV === 'development' ? dbError.message : undefined,
                    filters: {},
                    cars: [],
                    conversationId: conversationId || `conv_${Date.now()}`
                });
            }

            // Initialize filters object
            let filters = {};
            
            // First try to extract filters using AI
            try {
                const aiFilters = await extractFiltersWithAI(message);
                if (aiFilters) {
                    filters = { ...filters, ...aiFilters };
                    console.log('Extracted filters from AI:', aiFilters);
                }
            } catch (aiError) {
                console.warn('Error extracting filters with AI, falling back to simple extraction:', aiError);
            }
            
            // Then try to extract filters using regex patterns
            const regexFilters = extractFilters(message) || {};
            if (Object.keys(regexFilters).length > 0) {
                console.log('Extracted filters from regex:', regexFilters);
                filters = { ...filters, ...regexFilters };
            }
            
            console.log('Combined filters:', filters);

            // Check for car types with fuzzy matching for common misspellings
            const carTypeMap = {
                'sedan': 'SEDAN',
                'suv': 'SUV',
                'hatchback': 'HATCHBACK',
                'convertible': 'CONVERTIBLE',
                'converble': 'CONVERTIBLE',  // Common misspelling
                'convertable': 'CONVERTIBLE', // Common misspelling
                'truck': 'PICKUP',
                'pickup': 'PICKUP',
                'sports': 'SPORTS',
                'sport': 'SPORTS',
                'coupe': 'COUPE',
                'wagon': 'WAGON',
                'minivan': 'MINIVAN',
                'van': 'VAN',
                'electric': 'ELECTRIC',
                'hybrid': 'HYBRID',
                'roadster': 'ROADSTER',
                    'cabriolet': 'CABRIOLET'
                };

                // Try exact match first
                let carType = null;
                const words = message.toLowerCase().split(/\s+/);

                // Check each word against our type map
                for (const word of words) {
                    if (carTypeMap[word]) {
                        carType = carTypeMap[word];
                        break;
                    }
                }

            // If no exact match, try fuzzy match for common misspellings
            if (!carType) {
                for (const [key, value] of Object.entries(carTypeMap)) {
                    if (message.toLowerCase().includes(key)) {
                        carType = value;
                        break;
                    }
                }
            }

            if (carType) {
                filters = { ...filters, type: carType };
                console.log('Extracted car type from message:', carType);
            }

            // Apply filters to cars
            const filteredCars = filterCars(carData, filters);
            console.log(`Filtered ${filteredCars.length} cars out of ${carData.length}`);

            // Generate natural, context-aware response
            let finalResponse;
            const messageLower = message.toLowerCase().trim();
            const isGreeting = ['hello', 'hi', 'hey'].some(greeting => messageLower.startsWith(greeting));
            const isQuestion = messageLower.endsWith('?');
            const isAboutAI = /(are you (an ai|a bot)|you('re| are) (an ai|a bot)|is this ai)/i.test(message);
            const isConfused = /(what\?|huh|confused|don('|’)t understand)/i.test(message);

            // Handle different types of messages
            if (isGreeting) {
                finalResponse = [
                    "Hi there! I'm here to help you find your perfect car. What are you looking for?",
                    "Hello! Ready to find your dream car? What's on your wishlist?",
                    "Hey! I'd be happy to help you find a great vehicle. What type of car are you interested in?"
                ][Math.floor(Math.random() * 3)];
            }
            else if (isAboutAI) {
                finalResponse = [
                    "I'm here to help you find your perfect car. What kind of vehicle are you interested in?",
                    "I'm your car-finding assistant. Let me know what you're looking for in your next vehicle!",
                    "I'm here to help you explore our inventory. What features are most important to you in a car?"
                ][Math.floor(Math.random() * 3)];
            }
            else if (isConfused) {
                finalResponse = [
                    "I'm here to help you find a car. Could you tell me what you're looking for?",
                    "I want to make sure I understand. Could you tell me more about the type of car you need?",
                    "Let me help you better. What's most important to you in a vehicle?"
                ][Math.floor(Math.random() * 3)];
            }
            else if (filteredCars.length === 0) {
                // No cars found responses
                const suggestions = [
                    "What if we try a different color or price range?",
                    "Maybe we could look at similar models or different years?",
                    "Would you like to see what we have in a different category?",
                    "I can help you explore other options if you'd like."
                ];
                const randomSuggestion = suggestions[Math.floor(Math.random() * suggestions.length)];

                finalResponse = [
                    `I couldn't find any vehicles that match "${message}". ${randomSuggestion}`,
                    `Hmm, I don't see any matches for "${message}". ${randomSuggestion}`,
                    `No luck with "${message}". ${randomSuggestion}`
                ][Math.floor(Math.random() * 3)];
            }
            else {
                // Cars found - create a natural response
                const typeCounts = filteredCars.reduce((acc, car) => {
                    const type = car.type || 'vehicle';
                    acc[type] = (acc[type] || 0) + 1;
                    return acc;
                }, {});

                // Format type list naturally (e.g., "2 sedans, 1 SUV, 3 trucks")
                const typeList = Object.entries(typeCounts)
                    .map(([type, count]) => `${count} ${type.toLowerCase()}${count > 1 ? 's' : ''}`)
                    .join(', ');

                // Different response templates based on context and filters
                let searchTerm = 'vehicles';
                const type = filters?.type?.toLowerCase?.() || '';

                if (filters?.color && type) {
                    searchTerm = `${filters.color} ${type}${type.endsWith('s') ? '' : 's'}`;
                } else if (filters?.color) {
                    searchTerm = `${filters.color} cars`;
                } else if (type) {
                    searchTerm = `${type}${type.endsWith('s') ? '' : 's'}`;
                }

                // Clean up any duplicate words that might have come from the original message
                searchTerm = searchTerm.replace(/(\b\w+\b)(?=.*\b\1\b)/gi, '').replace(/\s+/g, ' ').trim();

                const responses = [
                    `I found ${filteredCars.length} ${searchTerm} for you.`,
                    `Here are ${filteredCars.length} ${searchTerm} in our inventory.`,
                    `I've got ${filteredCars.length} ${searchTerm} that might interest you.`,
                    `I found ${filteredCars.length} matching ${searchTerm} for you.`
                ];

                // Add type distribution if there are multiple types
                if (Object.keys(typeCounts).length > 1) {
                    responses[0] += ` There are ${typeList} available.`;
                    responses[1] += ` We have ${typeList} to choose from.`;
                    responses[2] += ` Including ${typeList}.`;
                    responses[3] += ` Available types: ${typeList}.`;
                }

                finalResponse = responses[Math.floor(Math.random() * responses.length)];

                // Add a relevant follow-up
                const followUps = [
                    " Would you like to know more about any of these?",
                    " Need help comparing any of these options?",
                    " Let me know if you'd like to see more details.",
                    " Interested in scheduling a test drive?"
                ];

                if (Math.random() < 0.4) { // 40% chance to add a follow-up
                    const followUp = followUps[Math.floor(Math.random() * followUps.length)];
                    finalResponse += followUp;
                }
            }

            // Add AI response to conversation history
            conversation.push({
                role: 'assistant',
                content: finalResponse,
                filters,
                matchingCars: filteredCars.length
            });

            // Update conversation history (keep last 10 messages)
            const trimmedConversation = conversation.slice(-10);
            conversationHistory.set(conversationId, trimmedConversation);

            // Log the interaction
            const newConversationId = await logInteraction(
                conversationId,
                message,
                finalResponse,
                filters,
                filteredCars
            );

            // Return the response
            res.json({
                message: finalResponse,
                filters,
                cars: filteredCars.slice(0, 20), // Limit number of cars sent to client
                conversationId: newConversationId,
                timestamp: new Date().toISOString()
            });

        } catch (error) {
            console.error('Error processing with Ollama:', error);
            // Fallback to simple filtering if AI fails
            const filters = extractFilters(message, carData || []);
            const filteredCars = filterCars(carData || [], filters);

            // Log the fallback interaction
            const newConversationId = await logInteraction(conversationId, message, 'Fallback response - AI processing failed', filters, filteredCars);

            res.json({
                role: 'assistant',
                content: "I'm having trouble with that request. Could you try rephrasing or asking something else?",
                error: process.env.NODE_ENV === 'development' ? error.message : undefined,
                filters: filters || {},
                cars: filteredCars,
                conversationId: newConversationId
            });
        }
    } catch (error) {
        console.error('Error in chat endpoint:', error);
        // Return a more helpful error message
        return res.status(200).json({
            role: 'assistant',
            content: "I'm having trouble with that request. Could you try rephrasing or asking something else?",
            error: process.env.NODE_ENV === 'development' ? error.message : undefined,
            filters: {},
            cars: [],
            conversationId: conversationId
        });
    }
});

// Enhanced filtering with AI
async function extractFiltersWithAI(message) {
    try {
        console.log('Extracting filters for message:', message);

        // First, check for price-related terms
        const priceTerms = {
            'cheap': 'budget',
            'affordable': 'budget',
            'budget': 'budget',
            'mid-range': 'midrange',
            'expensive': 'expensive',
            'luxury': 'luxury',
            'premium': 'premium'
        };

        // Check if message contains any price-related terms
        let priceRange = null;
        const lowerMessage = message.toLowerCase();
        
        for (const [term, range] of Object.entries(priceTerms)) {
            if (lowerMessage.includes(term)) {
                priceRange = range;
                break;
            }
        }
        
        // If we found a price range term, use it directly
        if (priceRange) {
            console.log(`Detected price range: ${priceRange}`);
            return { priceRange };
        }
        
        // Otherwise, use the AI for more complex queries
        const response = await axios.post(OLLAMA_API, {
            model: OLLAMA_MODEL,
            messages: [
                { 
                    role: 'system', 
                    content: FILTER_EXTRACTION_PROMPT
                },
                {
                    role: 'user',
                    content: `Extract filters from: "${message}"
                    
                    Return ONLY a JSON object with the filters. If no filters, return {}.`
                }
            ],
            response_format: { type: 'json_object' },
            temperature: 0.1
        });

        const result = response.data.choices[0].message.content;
        console.log('Raw AI response:', result);
        
        // Parse the response and ensure it's a valid object
        try {
            let filters = {};
            
            // Try to parse as JSON first
            if (typeof result === 'string') {
                // Handle cases where the response might be wrapped in markdown code blocks
                const jsonMatch = result.match(/```(?:json)?\n([\s\S]*?)\n```/);
                if (jsonMatch) {
                    filters = JSON.parse(jsonMatch[1]);
                } else if (result.trim().startsWith('{') && result.trim().endsWith('}')) {
                    filters = JSON.parse(result);
                } else {
                    console.log('No valid JSON found in response, using empty filters');
                    return {};
                }
            } else if (typeof result === 'object') {
                filters = result;
            }
            
            // Clean up the filters object
            const validFilters = {};
            const validFields = ['type', 'make', 'model', 'color', 'minPrice', 'maxPrice', 'minYear', 'maxYear'];
            
            // Convert all string values to lowercase and trim whitespace
            Object.entries(filters).forEach(([key, value]) => {
                if (validFields.includes(key) && value !== undefined && value !== null && value !== '') {
                    if (typeof value === 'string') {
                        validFilters[key] = value.toLowerCase().trim();
                    } else {
                        validFilters[key] = value;
                    }
                }
            });
            
            console.log('Extracted valid filters:', validFilters);
            return validFilters;
            
        } catch (parseError) {
            console.error('Error parsing AI response:', parseError);
            return {};
        }
    } catch (error) {
        console.error('Error extracting filters with AI:', error);
        return {}; // Return empty filters on error
    }
}

// Price range mappings for descriptive terms - adjusted to match actual inventory
const PRICE_RANGES = {
    'cheap': { maxPrice: 30000 },      // Under $30k
    'affordable': { maxPrice: 40000 },  // Under $40k
    'budget': { maxPrice: 40000 },      // Under $40k
    'midrange': { minPrice: 40001, maxPrice: 60000 },  // $40k - $60k
    'expensive': { minPrice: 60001 },   // Over $60k
    'luxury': { minPrice: 80000 },      // Over $80k
    'premium': { minPrice: 60001, maxPrice: 100000 }  // $60k - $100k
};

// Filter cars based on criteria
function filterCars(cars, filters) {
    if (!filters || Object.keys(filters).length === 0) {
        console.log('No filters to apply, returning all cars');
        return Array.isArray(cars) ? cars : [];
    }
    
    console.log('=== FILTERING CARS ===');
    console.log('Input filters:', JSON.stringify(filters, null, 2));
    
    // Handle price range terms first
    if (filters.priceRange) {
        console.log(`Processing price range: ${filters.priceRange}`);
        const range = PRICE_RANGES[filters.priceRange.toLowerCase()];
        if (range) {
            console.log(`Converted to price range:`, range);
            filters = { ...filters, ...range };
            delete filters.priceRange;
        } else {
            console.warn(`Unknown price range: ${filters.priceRange}`);
        }
    }
    
    // Get the array of cars or empty array if invalid
    const carArray = Array.isArray(cars) ? cars : [];
    
    console.log(`Filtering ${carArray.length} cars with filters:`, JSON.stringify(filters, null, 2));
    
    const filtered = carArray.filter(car => {
        if (!car || typeof car !== 'object') {
            console.log('Skipping invalid car:', car);
            return false;
        }
        
        // Log car being checked (first few for debugging)
        if (Math.random() < 0.1) { // Only log 10% of cars to avoid spam
            console.log('Checking car:', {
                id: car.id,
                model: car.model,
                type: car.type,
                price: car.price || car.dailyRate,
                year: car.year
            });
        }
        
        // Apply type filter if specified (handles both single type and array of types)
        if (filters.type) {
            const carType = String(car.type || '').toUpperCase();
            const filterTypes = Array.isArray(filters.type) ? filters.type : [filters.type];
            const matches = filterTypes.some(filterType => 
                carType.includes(String(filterType).toUpperCase())
            );
            if (!matches) {
                return false;
            }
        }
        
        // Apply color filter (case-insensitive partial match)
        if (filters.color && car.color) {
            const carColor = String(car.color).toLowerCase();
            const filterColor = String(filters.color).toLowerCase();
            if (!carColor.includes(filterColor)) {
                return false;
            }
        }
        
        // Apply price filter
        const price = Number(car.price) || Number(car.dailyRate) || 0;
        if (filters.minPrice !== undefined && price < Number(filters.minPrice)) {
            return false;
        }
        if (filters.maxPrice !== undefined && price > Number(filters.maxPrice)) {
            return false;
        }
        
        // Apply year filters
        const year = car.year ? Number(car.year) : 0;
        if (filters.minYear && year < Number(filters.minYear)) return false;
        if (filters.maxYear && year > Number(filters.maxYear)) return false;
        
        return true;
    });
    
    console.log(`Filtered to ${filtered.length} cars`);
    if (filtered.length > 0) {
        console.log('Sample of filtered cars:', filtered.slice(0, 3).map(c => ({
            id: c.id,
            model: c.model,
            type: c.type,
            price: c.price || c.dailyRate,
            year: c.year
        })));
    }
    
    return filtered;
}

// Log interactions for learning
async function logInteraction(conversationId, userMessage, aiResponse, filters = {}, results = []) {
    // Generate a new conversation ID if none provided
    const convId = conversationId || `conv_${Date.now()}`;
    
    try {
        await pool.query(
            'INSERT INTO chat_logs (conversation_id, user_message, ai_response, filters, results_count) VALUES (?, ?, ?, ?, ?)',
            [
                convId,
                userMessage || '',
                aiResponse || '',
                JSON.stringify(filters) || '{}',
                results?.length || 0
            ]
        );
        return convId; // Return the conversation ID for future reference
    } catch (error) {
        console.error('Error logging interaction:', error);
        return convId; // Still return the conversation ID even if logging fails
    }
}

function extractFilters(message) {
    const filters = {};
    const text = message.toLowerCase().trim();
    
    // Common car colors
    const colors = ['black', 'white', 'red', 'blue', 'silver', 'gray', 'grey', 'green', 'yellow', 'orange'];
    for (const color of colors) {
        if (text.includes(color)) {
            filters.color = color;
            break;
        }
    }
    
    // Extract car type
    const carTypes = ['sedan', 'suv', 'hatchback', 'convertible', 'sports', 'minivan', 'pickup', 'truck'];
    const typeMatch = carTypes.find(type => text.includes(type));
    if (typeMatch) {
        // Map some common variations to standard types
        const typeMap = {
            'sport': 'sports',
            'sportscar': 'sports',
            'sport car': 'sports',
            'pickup truck': 'pickup',
            'truck': 'pickup',
            'convert': 'convertible',
            'hatch': 'hatchback'
        };
        filters.type = typeMap[typeMatch] || typeMatch;
    }
    
    // Extract price range with better pattern matching
    const pricePatterns = [
        // Ranges: $20,000 to $30,000, 20k-30k, between 20 and 30k
        /(?:\$|€|£)?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)(?:\s*(?:to|-|and|–|between\s+)\s*(?:\$|€|£)?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)(?:k|\s*k)?)/i,
        // Under/over patterns: under $30k, less than 30000, over $20k
        /(under|below|less than|up to|over|above|more than|from)\s*(?:\$|€|£)?(\d{1,3}(?:,\d{3})*(?:\.\d{1,2})?)(?:k|\s*k)?/i
    ];
    
    for (const pattern of pricePatterns) {
        const match = text.match(pattern);
        if (match) {
            const parsePrice = (price) => {
                if (!price) return 0;
                const num = price.replace(/[^0-9.]/g, '');
                return num.endsWith('k') || (match[0].includes('k') && !match[0].includes('km') && !match[0].includes('kg')) 
                    ? parseFloat(num) * 1000 
                    : parseFloat(num);
            };
            
            if (match[1] && match[2]) {
                // Handle range patterns
                if (['under', 'below', 'less than', 'up to'].includes(match[1].toLowerCase())) {
                    filters.maxPrice = parsePrice(match[2]);
                } else if (['over', 'above', 'more than', 'from'].includes(match[1].toLowerCase())) {
                    filters.minPrice = parsePrice(match[2]);
                } else {
                    // Handle between X and Y pattern
                    filters.minPrice = parsePrice(match[1]);
                    filters.maxPrice = parsePrice(match[2]);
                }
            } else if (match[1]) {
                // Single price point
                filters.maxPrice = parsePrice(match[1]);
            }
            break;
        }
    }
    
    // Extract year range with better pattern matching
    const yearPatterns = [
        // Ranges: 2015-2020, from 2015 to 2020, between 2015 and 2020
        /(?:from\s+)?(20\d{2})\s*(?:to|-|and|–|through)\s*(20\d{2})/i,
        // Single year: 2020 model, year 2020, from 2020
        /(?:year|model|from)\s*(20\d{2})/i,
        // Just a 4-digit number that looks like a year
        /\b(20\d{2})\b/
    ];
    
    for (const pattern of yearPatterns) {
        const match = text.match(pattern);
        if (match) {
            const currentYear = new Date().getFullYear();
            
            if (match[2]) {
                // It's a range
                const year1 = parseInt(match[1]);
                const year2 = parseInt(match[2]);
                if (year1 >= 1990 && year1 <= currentYear + 1 && 
                    year2 >= 1990 && year2 <= currentYear + 1) {
                    filters.minYear = Math.min(year1, year2);
                    filters.maxYear = Math.max(year1, year2);
                }
            } else if (match[1]) {
                // It's a single year
                const year = parseInt(match[1]);
                if (year >= 1990 && year <= currentYear + 1) {
                    filters.year = year;
                }
            }
            break;
        }
    }
    
    // Extract transmission type with more variations
    if (text.match(/\bauto(?:matic)?\b/i)) {
        filters.transmission = 'automatic';
    } else if (text.match(/\bman(?:ual)?\b|\bstick(?: shift)?\b|\bstandard(?: transmission)?\b/i)) {
        filters.transmission = 'manual';
    }
    
    // Extract make and model (simple pattern)
    const makeModelPatterns = [
        // Common makes
        /(bmw|mercedes|audi|toyota|honda|ford|chevrolet|nissan|hyundai|kia|volkswagen|volvo|subaru|mazda|lexus|tesla|porsche|ferrari|lamborghini|bentley|rolls-royce|jaguar|land rover|jeep|ram|gmc|dodge|chrysler|buick|cadillac|lincoln|acura|infiniti|genesis|mini|fiat|alfa romeo|maserati|mclaren|bugatti|koenigsegg|pagani|lotus|aston martin|morgan|bentley|rolls royce|landrover)/i,
        // Model patterns (3 series, f-150, etc.)
        /(?:bmw\s*(\d+\s*series?)?|mercedes[-\s]?(?:benz)?\s*([a-z]\s*\d+)|audi\s*([a-z]\s*\d+)|(\w+)\s*(\d{3,})|(\w+)\s*([a-z]\s*\d+))/i
    ];
    
    for (const pattern of makeModelPatterns) {
        const match = text.match(pattern);
        if (match) {
            const potentialMake = match[1] || match[4] || match[6];
            const potentialModel = match[2] || match[3] || match[5] || match[7];
            
            if (potentialMake && !filters.make) {
                filters.make = potentialMake.trim();
            }
            if (potentialModel && !filters.model) {
                filters.model = potentialModel.trim();
            }
            
            if (filters.make || filters.model) break;
        }
    }
    
    // Clean up the filters
    Object.keys(filters).forEach(key => {
        if (filters[key] === undefined || filters[key] === '') {
            delete filters[key];
        } else if (typeof filters[key] === 'string') {
            // Remove extra spaces and special characters
            filters[key] = filters[key].replace(/\s+/g, ' ').trim();
        }
    });
    
    console.log('Extracted filters:', filters); // Debug log
    return Object.keys(filters).length > 0 ? filters : null;
}

app.listen(PORT, () => {
    console.log(`AI Service running on http://localhost:${PORT}`);
});
