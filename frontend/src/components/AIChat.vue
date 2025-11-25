<template>
  <div class="ai-chat">
    <button v-if="!isOpen" @click="toggleChat" class="chat-button">
      <span class="chat-icon">🤖</span>
    </button>
    
    <div v-else class="chat-container">
      <div class="chat-header">
        <h3>Car Assistant</h3>
        <button @click="toggleChat" class="close-button">×</button>
      </div>
      
      <div class="messages" ref="messages">
        <div v-for="(msg, i) in messages" :key="i" :class="['message', msg.sender]">
          <div class="message-content">{{ msg.text }}</div>
        </div>
        <div v-if="isLoading" class="typing-indicator">
          <span></span><span></span><span></span>
        </div>
      </div>
      
      <div class="input-area">
        <input
          v-model="userInput"
          @keyup.enter="sendMessage"
          placeholder="Ask about available cars..."
          :disabled="isLoading"
        />
        <button @click="sendMessage" :disabled="!userInput.trim() || isLoading">
          Send
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AIChat',
  props: {
    cars: {
      type: Array,
      default: () => []
    }
  },
  data() {
    return {
      isOpen: false,
      userInput: '',
      messages: [
        { 
          sender: 'ai', 
          text: 'Hello! I can help you find your perfect car. What are you looking for?' 
        }
      ],
      isLoading: false
    };
  },
  methods: {
    toggleChat() {
      this.isOpen = !this.isOpen;
      if (this.isOpen) {
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },
    async sendMessage() {
      const message = this.userInput.trim();
      if (!message) return;

      this.messages.push({ sender: 'user', text: message });
      this.userInput = '';
      this.isLoading = true;

      try {
        // Log the cars we're sending to the backend
        console.log('Sending cars to AI service:', this.cars);
        
        // Include car data with the message
        const requestData = {
          message: message,
          cars: this.cars.map(car => ({
            id: car.id,
            make: car.make,
            model: car.model,
            type: car.type,
            year: car.year,
            price: car.price,
            dailyRate: car.dailyRate,
            transmission: car.transmission,
            // Include any other necessary car fields
            ...car
          }))
        };
        
        const response = await fetch('http://localhost:3001/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(requestData)
        });

        const responseData = await response.json();
        console.log('AI Response:', responseData); // Debug log

        if (!response.ok) {
          throw new Error(responseData.error || 'Failed to get response');
        }

        // Add AI response to messages
        this.messages.push({
          sender: 'ai',
          text: responseData.message || responseData.response || 'I found some cars that might interest you.'
        });

        // If we have filtered cars in the response, update the parent
        if (responseData.cars && Array.isArray(responseData.cars)) {
          console.log('Emitting updated cars:', responseData.cars);
          // First emit the filters
          if (responseData.filters) {
            console.log('Emitting filters:', responseData.filters);
            this.$emit('apply-filters', responseData.filters);
          }
          // Then emit the filtered cars
          this.$nextTick(() => {
            this.$emit('update:cars', responseData.cars);
          });
        } else if (responseData.filters) {
          // If we only have filters, still emit them
          console.log('Emitting only filters:', responseData.filters);
          this.$emit('apply-filters', responseData.filters);
        }

      } catch (error) {
        console.error('Error:', error);
        this.messages.push({
          sender: 'ai',
          text: 'Sorry, I encountered an error. Please try again.'
        });
      } finally {
        this.isLoading = false;
        this.scrollToBottom();
      }
    },
    scrollToBottom() {
      this.$nextTick(() => {
        const container = this.$refs.messages;
        if (container) {
          container.scrollTop = container.scrollHeight;
        }
      });
    }
  },
  watch: {
    isOpen() {
      this.scrollToBottom();
    }
  }
};
</script>

<style scoped>
.ai-chat {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
}

.chat-button {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: #4a6cf7;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.chat-button:hover {
  transform: scale(1.1);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
}

.chat-container {
  width: 350px;
  max-width: 90vw;
  height: 500px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: #4a6cf7;
  color: white;
  padding: 15px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chat-header h3 {
  margin: 0;
  font-size: 16px;
  font-weight: 600;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 0 5px;
  line-height: 1;
  opacity: 0.8;
  transition: opacity 0.2s;
}

.close-button:hover {
  opacity: 1;
}

.messages {
  flex: 1;
  padding: 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.message {
  max-width: 80%;
  padding: 10px 15px;
  border-radius: 15px;
  line-height: 1.4;
  position: relative;
}

.message.user {
  align-self: flex-end;
  background: #e3f2fd;
  border-bottom-right-radius: 5px;
}

.message.ai {
  align-self: flex-start;
  background: #f5f5f5;
  border-bottom-left-radius: 5px;
}

.input-area {
  padding: 15px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
}

.input-area input {
  flex: 1;
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 20px;
  outline: none;
  font-size: 14px;
}

.input-area input:focus {
  border-color: #4a6cf7;
}

.input-area button {
  padding: 0 20px;
  background: #4a6cf7;
  color: white;
  border: none;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: background 0.2s;
}

.input-area button:hover:not(:disabled) {
  background: #3a5bd9;
}

.input-area button:disabled {
  background: #a8b8f8;
  cursor: not-allowed;
}

.typing-indicator {
  display: flex;
  gap: 5px;
  padding: 10px;
  align-self: flex-start;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: #888;
  border-radius: 50%;
  display: inline-block;
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { 
    transform: scale(0);
    opacity: 0.5;
  } 
  40% { 
    transform: scale(1);
    opacity: 1;
  }
}

/* Custom scrollbar */
.messages::-webkit-scrollbar {
  width: 6px;
}

.messages::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.messages::-webkit-scrollbar-thumb {
  background: #c1c1c1;
  border-radius: 3px;
}

.messages::-webkit-scrollbar-thumb:hover {
  background: #a8a8a8;
}
</style>
