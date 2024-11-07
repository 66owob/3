from lib import 初始化資料庫, 匯入資料, 查詢電影, 新增電影, 修改電影, 刪除電影, 匯出資料

def main():
    # 自動初始化資料庫
    初始化資料庫()

    while True:
        print("\n--- 電影管理系統 ---")
        print("1. 匯入電影資料")
        print("2. 查詢電影")
        print("3. 新增電影")
        print("4. 修改電影")
        print("5. 刪除電影")
        print("6. 匯出電影")
        print("0. 離開")

        choice = input("請選擇功能: ")

        if choice == '1':
            匯入資料()
        elif choice == '2':
            title = input("輸入欲查詢的電影名稱 (留空則查詢全部): ")
            查詢電影(title)
        elif choice == '3':
            新增電影()
        elif choice == '4':
            title = input("輸入欲修改的電影名稱: ")
            修改電影(title)
        elif choice == '5':
            title = input("輸入欲刪除的電影名稱 (留空則刪除全部): ")
            刪除電影(title)
        elif choice == '6':
            title = input("輸入欲匯出的電影名稱 (留空則匯出全部): ")
            匯出資料(title)
        elif choice == '0':
            print("系統結束。")
            break
        else:
            print("無效的選項，請重新選擇。")

if __name__ == "__main__":
    main()
