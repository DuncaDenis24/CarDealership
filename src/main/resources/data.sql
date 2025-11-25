-- Clear existing data
DELETE FROM cars;

-- TRUNCATE TABLE cars; -- Recomandat să ștergi datele vechi înainte de a le insera pe cele noi

INSERT INTO cars (name, model, color, manufacture_year, license_plate, daily_rate, price, type, is_available, is_for_sale, is_for_rent, image_url) VALUES
-- ====================================================================================
-- 1. SEDANS (20 Entries)
-- ====================================================================================
('Toyota', 'Camry', 'Midnight Black', 2023, 'TOY001', 55.00, 25000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/103290/pexels-photo-103290.jpeg?w=600'),
('Honda', 'Accord', 'Crystal Black Pearl', 2023, 'HON001', 50.00, 27000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/112460/pexels-photo-112460.jpeg?w=600'),
('BMW', '3 Series', 'Alpine White', 2023, 'BMW003', 85.00, 42000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/17698305/pexels-photo-17698305.jpeg?w=600'),
('Mercedes', 'E-Class', 'Selenite Grey', 2023, 'MERC02', 95.00, 55000.00, 'SEDAN', true, false, true, 'https://images.pexels.com/photos/9944061/pexels-photo-9944061.jpeg?w=600'),
('Audi', 'A6', 'Navarra Blue', 2023, 'AUDI02', 90.00, 52000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/13350774/pexels-photo-13350774.jpeg?w=600'),
('Tesla', 'Model S', 'Pearl White', 2023, 'TES002', 150.00, 90000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/909907/pexels-photo-909907.jpeg?w=600'),
('Tesla', 'Model 3', 'Midnight Silver', 2023, 'TES001', 120.00, 45000.00, 'SEDAN', true, true, false, 'https://images.pexels.com/photos/11082539/pexels-photo-11082539.jpeg?w=600'),
('Porsche', 'Taycan', 'Mamba Green', 2023, 'POR002', 230.00, 105000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/13591461/pexels-photo-13591461.jpeg?w=600'),
('Mercedes', 'S-Class', 'Obsidian Black', 2023, 'MERC04', 200.00, 110000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/14847847/pexels-photo-14847847.jpeg?w=600'),
('BMW', '7 Series', 'Carbon Black', 2023, 'BMW004', 190.00, 105000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/16382767/pexels-photo-16382767.jpeg?w=600'),
('Audi', 'A8', 'Florett Silver', 2023, 'AUDI06', 195.00, 108000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/18260655/pexels-photo-18260655.jpeg?w=600'),
('Lexus', 'LS', 'Matador Red Mica', 2023, 'LEX001', 180.00, 95000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/16140416/pexels-photo-16140416.jpeg?w=600'),
('Genesis', 'G90', 'Havana Red', 2023, 'GEN001', 170.00, 88000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/18449969/pexels-photo-18449969.jpeg?w=600'),
('Volvo', 'S60', 'Osmium Grey', 2023, 'VOL001', 70.00, 35000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/18413647/pexels-photo-18413647.jpeg?w=600'),
('Kia', 'Stinger', 'Ceramic Silver', 2023, 'KIA001', 80.00, 38000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/16382767/pexels-photo-16382767.jpeg?w=600'),
('Mazda', 'Mazda6', 'Soul Red Crystal', 2023, 'MAZ001', 60.00, 28000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/337909/pexels-photo-337909.jpeg?w=600'),
('Hyundai', 'Elantra', 'Intense Blue', 2023, 'HYU002', 45.00, 22000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/16652873/pexels-photo-16652873.jpeg?w=600'),
('Volkswagen', 'Passat', 'Deep Black Pearl', 2023, 'VW003', 50.00, 26000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/103290/pexels-photo-103290.jpeg?w=600'),
('Jaguar', 'XF', 'Loire Blue', 2023, 'JAG001', 110.00, 58000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/112460/pexels-photo-112460.jpeg?w=600'),
('Chrysler', '300', 'Granite Crystal', 2023, 'CHR001', 65.00, 30000.00, 'SEDAN', true, true, true, 'https://images.pexels.com/photos/9944061/pexels-photo-9944061.jpeg?w=600'),

-- ====================================================================================
-- 2. SUVS (15 Entries)
-- ====================================================================================
('Toyota', 'RAV4', 'Ruby Flare Pearl', 2023, 'TOY002', 65.00, 32000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/707047/pexels-photo-707047.jpeg?w=600'),
('Honda', 'CR-V', 'Sonic Gray Pearl', 2023, 'HON002', 60.00, 30000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/2039989/pexels-photo-2039989.jpeg?w=600'),
('BMW', 'X5', 'Phytonic Blue', 2023, 'BMW001', 120.00, 65000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/1879799/pexels-photo-1879799.jpeg?w=600'),
('Mercedes', 'GLE', 'Obsidian Black', 2023, 'MERC03', 130.00, 68000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/3802510/pexels-photo-3802510.jpeg?w=600'),
('Audi', 'Q7', 'Florett Silver', 2023, 'AUDI03', 125.00, 67000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/13591461/pexels-photo-13591461.jpeg?w=600'),
('Tesla', 'Model X', 'Red Multi-Coat', 2023, 'TES003', 170.00, 95000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/11082539/pexels-photo-11082539.jpeg?w=600'),
('Audi', 'e-tron', 'Glacier White', 2023, 'AUDI05', 160.00, 75000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/13350774/pexels-photo-13350774.jpeg?w=600'),
('Jeep', 'Grand Cherokee', 'Bright White', 2023, 'JEEP01', 80.00, 45000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/18413647/pexels-photo-18413647.jpeg?w=600'),
('Subaru', 'Forester', 'Autumn Green Metallic', 2023, 'SUB001', 65.00, 33000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/337909/pexels-photo-337909.jpeg?w=600'),
('Ford', 'Explorer', 'Star White Metallic', 2023, 'FORD03', 90.00, 50000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/16652873/pexels-photo-16652873.jpeg?w=600'),
('Volvo', 'XC90', 'Denim Blue', 2023, 'VOL002', 110.00, 62000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/3802510/pexels-photo-3802510.jpeg?w=600'),
('Land Rover', 'Defender', 'Pangea Green', 2023, 'LR001', 140.00, 75000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/707047/pexels-photo-707047.jpeg?w=600'),
('Kia', 'Sportage', 'Fusion Black', 2023, 'KIA002', 55.00, 29000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/2039989/pexels-photo-2039989.jpeg?w=600'),
('Mitsubishi', 'Outlander', 'Red Diamond', 2023, 'MIT001', 50.00, 28000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/1879799/pexels-photo-1879799.jpeg?w=600'),
('Nissan', 'Rogue', 'Pearl White', 2023, 'NIS002', 58.00, 31000.00, 'SUV', true, true, true, 'https://images.pexels.com/photos/3802510/pexels-photo-3802510.jpeg?w=600'),

-- ====================================================================================
-- 3. SPORTS CARS (10 Entries)
-- ====================================================================================
('Porsche', '911', 'Guards Red', 2023, 'POR001', 250.00, 120000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/1108170/pexels-photo-1108170.jpeg?w=600'),
('Chevrolet', 'Corvette', 'Arctic White', 2023, 'CHEVY01', 220.00, 85000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/1035108/pexels-photo-1035108.jpeg?w=600'),
('Nissan', 'GT-R', 'Bayside Blue', 2023, 'NIS001', 280.00, 115000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/15743438/pexels-photo-15743438.jpeg?w=600'),
('BMW', 'M4', 'Sao Paulo Yellow', 2023, 'BMW002', 200.00, 75000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/17698305/pexels-photo-17698305.jpeg?w=600'),
('Audi', 'R8', 'Daytona Gray', 2023, 'AUDI04', 300.00, 150000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/13350774/pexels-photo-13350774.jpeg?w=600'),
('Ford', 'Mustang GT', 'Velocity Blue', 2023, 'FORD04', 180.00, 60000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/120049/pexels-photo-120049.jpeg?w=600'),
('Dodge', 'Challenger Hellcat', 'TorRed', 2023, 'DODG01', 210.00, 80000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/1035108/pexels-photo-1035108.jpeg?w=600'),
('Jaguar', 'F-Type', 'Fuji White', 2023, 'JAG002', 190.00, 70000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/120049/pexels-photo-120049.jpeg?w=600'),
('Mazda', 'MX-5 Miata', 'Machine Gray', 2023, 'MAZ002', 100.00, 35000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/15743438/pexels-photo-15743438.jpeg?w=600'),
('Lexus', 'LC 500', 'Infrared', 2023, 'LEX002', 240.00, 100000.00, 'SPORTS', true, true, true, 'https://images.pexels.com/photos/1108170/pexels-photo-1108170.jpeg?w=600'),

-- ====================================================================================
-- 4. HATCHBACKS (5 Entries)
-- ====================================================================================
('Volkswagen', 'Golf GTI', 'Tornado Red', 2023, 'VW002', 55.00, 32000.00, 'HATCHBACK', true, true, true, 'https://images.pexels.com/photos/17698305/pexels-photo-17698305.jpeg?w=600'),
('Honda', 'Civic Type R', 'Championship White', 2023, 'HON003', 65.00, 38000.00, 'HATCHBACK', true, true, true, 'https://images.pexels.com/photos/112460/pexels-photo-112460.jpeg?w=600'),
('Toyota', 'Corolla Hatchback', 'Blue Flame', 2023, 'TOY003', 50.00, 28000.00, 'HATCHBACK', true, true, true, 'https://images.pexels.com/photos/103290/pexels-photo-103290.jpeg?w=600'),
('Hyundai', 'Veloster N', 'Performance Blue', 2023, 'HYU001', 60.00, 35000.00, 'HATCHBACK', true, true, true, 'https://images.pexels.com/photos/16652873/pexels-photo-16652873.jpeg?w=600'),
('Mini', 'Cooper S', 'British Racing Green', 2023, 'MINI01', 70.00, 32000.00, 'HATCHBACK', true, true, true, 'https://images.pexels.com/photos/337909/pexels-photo-337909.jpeg?w=600'),

-- ====================================================================================
-- 5. PICKUP TRUCKS (5 Entries)
-- ====================================================================================
('Ford', 'F-150 Raptor', 'Code Orange', 2023, 'FORD02', 120.00, 75000.00, 'PICKUP', true, true, true, 'https://images.pexels.com/photos/1035108/pexels-photo-1035108.jpeg?w=600'),
('Chevrolet', 'Silverado 1500', 'Northsky Blue', 2023, 'CHEVY02', 110.00, 68000.00, 'PICKUP', true, true, true, 'https://images.pexels.com/photos/1879799/pexels-photo-1879799.jpeg?w=600'),
('Ram', '1500 TRX', 'Hydro Blue', 2023, 'RAM001', 140.00, 85000.00, 'PICKUP', true, true, true, 'https://images.pexels.com/photos/707047/pexels-photo-707047.jpeg?w=600'),
('Toyota', 'Tacoma TRD Pro', 'Lunar Rock', 2023, 'TOY004', 95.00, 55000.00, 'PICKUP', true, true, true, 'https://images.pexels.com/photos/2039989/pexels-photo-2039989.jpeg?w=600'),
('GMC', 'Sierra 1500', 'Titanium Rush', 2023, 'GMC001', 115.00, 70000.00, 'PICKUP', true, true, true, 'https://images.pexels.com/photos/3802510/pexels-photo-3802510.jpeg?w=600'),

-- ====================================================================================
-- 6. CONVERTIBLES (5 Entries)
-- ====================================================================================
('BMW', '4 Series Convertible', 'Sanremo Green', 2023, 'BMW005', 150.00, 65000.00, 'CONVERTIBLE', true, true, true, 'https://images.pexels.com/photos/17698305/pexels-photo-17698305.jpeg?w=600'),
('Mercedes', 'E-Class Cabriolet', 'Selenite Grey', 2023, 'MERC05', 160.00, 78000.00, 'CONVERTIBLE', true, true, true, 'https://images.pexels.com/photos/14847847/pexels-photo-14847847.jpeg?w=600'),
('Porsche', '911 Cabriolet', 'Gentian Blue', 2023, 'POR003', 280.00, 125000.00, 'CONVERTIBLE', true, true, true, 'https://images.pexels.com/photos/1108170/pexels-photo-1108170.jpeg?w=600'),
('Chevrolet', 'Camaro Convertible', 'Shock', 2023, 'CHEVY03', 130.00, 55000.00, 'CONVERTIBLE', true, true, true, 'https://images.pexels.com/photos/1035108/pexels-photo-1035108.jpeg?w=600'),
('Audi', 'A5 Cabriolet', 'Tango Red', 2023, 'AUDI07', 140.00, 62000.00, 'CONVERTIBLE', true, true, true, 'https://images.pexels.com/photos/13350774/pexels-photo-13350774.jpeg?w=600');