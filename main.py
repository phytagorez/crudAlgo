import psycopg2
import pandas as pd

#Connect DB
def connectDB():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            user="postgres",
            password="23",
            dbname="db_coffeshop"
        )

        cur = conn.cursor()

        return conn, cur

    except Exception as error:
        print("Koneksi database gagal:", error)
        return None, None
    
#Validation
# conn, cur = connectDB()

# if conn is not None:
#     print("Berhasil terhubung ke PostgreSQL!")

#     cur.close()
#     conn.close()
# else:
#     print("Gagal terhubung ke database.")
    

def addBahan(nama_bahan, kategori, stok, satuan, harga_satuan):
    conn, cur = connectDB()

    try:
        query_insert = """
            INSERT INTO bahan_baku
            (nama_bahan, kategori, stok, satuan, harga_satuan)
            VALUES (%s, %s, %s, %s, %s)
        """

        cur.execute(query_insert, (
            nama_bahan,
            kategori,
            stok,
            satuan,
            harga_satuan
        ))

        conn.commit()
        print("Data bahan berhasil ditambahkan!")

    except Exception as error:
        conn.rollback()
        print("Gagal menambahkan data:", error)

    finally:
        cur.close()
        conn.close()
        
def getAllBahan():
    conn, cur = connectDB()

    try:
        query_select = """
            SELECT * FROM bahan_baku
            ORDER BY id_bahan
        """

        cur.execute(query_select)

        data = cur.fetchall()

        data = pd.DataFrame(data, columns=[
            "id_bahan",
            "nama_bahan",
            "kategori",
            "stok",
            "satuan",
            "harga_satuan"
        ])

        data.index += 1

        return data

    finally:
        cur.close()
        conn.close()
        
def updateDataBahan(id_bahan, nama_bahan, kategori,
                    stok, satuan, harga_satuan):

    conn, cur = connectDB()

    try:
        query_update = """
            UPDATE bahan_baku
            SET nama_bahan = %s,
                kategori = %s,
                stok = %s,
                satuan = %s,
                harga_satuan = %s
            WHERE id_bahan = %s
        """

        cur.execute(query_update, (
            nama_bahan,
            kategori,
            stok,
            satuan,
            harga_satuan,
            id_bahan
        ))

        jumlah = cur.rowcount

        conn.commit()

        print(f"{jumlah} data berhasil diperbarui.")

    except Exception as error:
        conn.rollback()
        print("Gagal memperbarui data:", error)

    finally:
        cur.close()
        conn.close()

def deleteBahanById(id_bahan):
    conn, cur = connectDB()

    try:
        query_delete = """
            DELETE FROM bahan_baku
            WHERE id_bahan = %s
        """

        cur.execute(query_delete, (id_bahan,))

        jumlah = cur.rowcount

        conn.commit()

        print(f"{jumlah} data berhasil dihapus.")

    except Exception as error:
        conn.rollback()
        print("Gagal menghapus data:", error)

    finally:
        cur.close()
        conn.close()
        
def menuUtama():
    while True:
        print("[1] Lihat Data Bahan")
        print("[2] Tambah Bahan")
        print("[3] Ubah Data Bahan")
        print("[4] Hapus Bahan")
        print("[5] Analisis Stok")
        print("[0] Keluar")

        pilihan = input("\nMasukkan pilihan: ")

        match pilihan:
            case "1":
                data = getAllBahan()
                print(data.to_string())

            case "2":
                nama = input("Nama bahan: ")
                kategori = input("Kategori: ")
                stok = int(input("Jumlah stok: "))
                satuan = input("Satuan: ")
                harga = int(input("Harga per satuan: "))

                addBahan(nama, kategori, stok, satuan, harga)

            case "3":
                print(getAllBahan().to_string())

                id_bahan = int(input("ID bahan: "))
                nama = input("Nama baru: ")
                kategori = input("Kategori baru: ")
                stok = int(input("Stok baru: "))
                satuan = input("Satuan: ")
                harga = int(input("Harga baru: "))

                updateDataBahan(
                    id_bahan, nama, kategori,
                    stok, satuan, harga
                )

            case "4":
                print(getAllBahan().to_string())

                id_bahan = int(input("ID bahan: "))
                konfirmasi = input("Yakin hapus? (y/n): ")

                if konfirmasi.lower() == "y":
                    deleteBahanById(id_bahan)

            case "5":
                data = getAllBahan()

                data["nilai_persediaan"] = (
                    data["stok"] * data["harga_satuan"]
                )

                print(data.to_string())
                print(
                    "\nTotal nilai persediaan: Rp",
                    data["nilai_persediaan"].sum()
                )

            case "0":
                print("Terima kasih!")
                break

            case _:
                print("Pilihan tidak valid!")

        if pilihan != "0":
            input("\nTekan Enter untuk melanjutkan...")
            
            
menuUtama()