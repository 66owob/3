import sqlite3
import json
import os

# 資料庫名稱
DATABASE_NAME = 'movies.db'

def 初始化資料庫():
    """檢查資料庫是否存在，若不存在則建立資料庫及資料表。"""
    if not os.path.exists(DATABASE_NAME):
        print("找不到資料庫，正在建立資料庫及資料表...")
        建立資料表()
    else:
        print("資料庫已存在。")

def 建立資料表():
    """建立 movies 資料表。"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                director TEXT NOT NULL,
                genre TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL CHECK(rating >= 1.0 AND rating <= 10.0)
            )
        ''')
        conn.commit()
        print("資料表建立成功。")
    except sqlite3.Error as e:
        print(f"建立資料表錯誤: {e}")
    finally:
        conn.close()

def 匯入資料():
    """從 movies.json 檔案匯入電影資料。"""
    if not os.path.exists("movies.json"):
        print("找不到 movies.json 檔案。")
        return

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        with open("movies.json", 'r', encoding='utf-8') as file:
            movies = json.load(file)
            for movie in movies:
                cursor.execute('''
                    INSERT INTO movies (title, director, genre, year, rating)
                    VALUES (?, ?, ?, ?, ?)
                ''', (movie['title'], movie['director'], movie['genre'], movie['year'], movie['rating']))

        conn.commit()
        print("資料匯入成功。")
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        conn.close()

def 查詢電影(title=None):
    """查詢全部電影或根據片名查詢電影。"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        if title:
            cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + title + '%',))
        else:
            cursor.execute("SELECT * FROM movies")

        movies = cursor.fetchall()

        for movie in movies:
            print(f"ID: {movie[0]}, 片名: {movie[1]}, 導演: {movie[2]}, 類型: {movie[3]}, 年份: {movie[4]}, 評分: {movie[5]}")
    except sqlite3.Error as e:
        print(f"查詢電影錯誤: {e}")
    finally:
        conn.close()

def 新增電影():
    """新增電影資料，並檢查年份與評分格式。"""
    title = input("輸入電影名稱: ")
    director = input("輸入導演: ")
    genre = input("輸入類型: ")

    while True:
        try:
            year = int(input("輸入年份: "))
            break
        except ValueError:
            print("年份必須是整數，請重新輸入。")

    while True:
        try:
            rating = float(input("輸入評分 (1.0 - 10.0): "))
            if 1.0 <= rating <= 10.0:
                break
            else:
                print("評分必須在 1.0 到 10.0 之間。")
        except ValueError:
            print("評分必須是數值，請重新輸入。")

    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO movies (title, director, genre, year, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, director, genre, year, rating))
        conn.commit()
        print("電影新增成功。")
    except sqlite3.Error as e:
        print(f"新增電影錯誤: {e}")
    finally:
        conn.close()

def 修改電影(title):
    """根據電影名稱修改資料，若欄位未輸入新值則保持原值。"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM movies WHERE title = ?", (title,))
        movie = cursor.fetchone()

        if not movie:
            print("找不到指定的電影。")
            return

        print(f"目前資料 - ID: {movie[0]}, 片名: {movie[1]}, 導演: {movie[2]}, 類型: {movie[3]}, 年份: {movie[4]}, 評分: {movie[5]}")

        new_title = input(f"輸入新片名（保持不變: {movie[1]}): ") or movie[1]
        new_director = input(f"輸入新導演（保持不變: {movie[2]}): ") or movie[2]
        new_genre = input(f"輸入新類型（保持不變: {movie[3]}): ") or movie[3]

        new_year = input(f"輸入新年份（保持不變: {movie[4]}): ")
        if new_year:
            new_year = int(new_year)
        else:
            new_year = movie[4]

        new_rating = input(f"輸入新評分（保持不變: {movie[5]}): ")
        if new_rating:
            new_rating = float(new_rating)
        else:
            new_rating = movie[5]

        cursor.execute('''
            UPDATE movies
            SET title = ?, director = ?, genre = ?, year = ?, rating = ?
            WHERE id = ?
        ''', (new_title, new_director, new_genre, new_year, new_rating, movie[0]))

        conn.commit()
        print("電影修改成功。")
    except sqlite3.Error as e:
        print(f"修改電影錯誤: {e}")
    except ValueError:
        print("輸入格式錯誤，請檢查年份和評分格式。")
    finally:
        conn.close()

def 刪除電影(title=None):
    """刪除全部電影或根據片名刪除電影。"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        if title:
            cursor.execute("DELETE FROM movies WHERE title = ?", (title,))
            print(f"已刪除電影: {title}")
        else:
            cursor.execute("DELETE FROM movies")
            print("已刪除全部電影。")

        conn.commit()
    except sqlite3.Error as e:
        print(f"刪除電影錯誤: {e}")
    finally:
        conn.close()

def 匯出資料(title=None):
    """匯出全部或指定電影至 exported.json。"""
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()

        if title:
            cursor.execute("SELECT * FROM movies WHERE title LIKE ?", ('%' + title + '%',))
        else:
            cursor.execute("SELECT * FROM movies")

        movies = cursor.fetchall()

        with open("exported.json", 'w', encoding='utf-8') as file:
            json.dump([{
                "id": movie[0],
                "title": movie[1],
                "director": movie[2],
                "genre": movie[3],
                "year": movie[4],
                "rating": movie[5]
            } for movie in movies], file, ensure_ascii=False, indent=4)

        print("資料匯出成功。")
    except sqlite3.Error as e:
        print(f"資料庫錯誤: {e}")
    except Exception as e:
        print(f"錯誤: {e}")
    finally:
        conn.close()
