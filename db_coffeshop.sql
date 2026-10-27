CREATE TABLE bahan_baku (
    id_bahan SERIAL PRIMARY KEY,
    nama_bahan VARCHAR(100) NOT NULL,
    kategori VARCHAR(50) NOT NULL,
    stok INTEGER NOT NULL CHECK (stok >= 0),
    satuan VARCHAR(20) NOT NULL,
    harga_satuan INTEGER NOT NULL CHECK (harga_satuan >= 0)
);

INSERT INTO bahan_baku
(nama_bahan, kategori, stok, satuan, harga_satuan)
VALUES
('Biji Kopi Arabika', 'Kopi', 5000, 'gram', 180),
('Susu UHT', 'Susu', 12000, 'ml', 20),
('Sirup Vanilla', 'Sirup', 3000, 'ml', 90),
('Gula Aren', 'Pemanis', 4000, 'gram', 35),
('Bubuk Matcha', 'Bubuk', 1500, 'gram', 350); 

select * from bahan_baku