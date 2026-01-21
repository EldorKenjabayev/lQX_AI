
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_edu_center_data():
    """
    Kichik O'quv Markazi (2026)
    - 12 ta kompyuter (1 xona)
    - 4-5 guruh kuniga
    - O'quvchi to'lovi: 400,000 - 600,000 UZS (o'rtacha 500k)
    - Xarajatlar: Arenda, O'qituvchi oyligi (KPI), Kommunal, Internet
    """
    start_date = datetime(2026, 1, 1)
    days = 60 # 2 oy
    data = []
    
    # Parametrlari
    groups_count = 4
    students_per_group = 10 # o'rtacha to'la emas
    total_students = groups_count * students_per_group
    monthly_fee = 500000 
    
    # Arenda (Toshkent, kichik ofis): ~$500 => ~6.5 mln UZS
    rent_cost = 6500000
    
    # O'qituvchi oyligi: Tushumning 40%
    teacher_share = 0.4
    
    current_date = start_date
    for i in range(days):
        date_str = current_date.strftime('%Y-%m-%d')
        is_weekend = current_date.weekday() >= 5
        
        # 1. KIRIM (To'lovlar)
        # Ota-onalar odatda oy boshida to'laydi (1-10 sanalar)
        day_of_month = current_date.day
        if 1 <= day_of_month <= 10:
            # Kuniga 3-5 ta o'quvchi to'laydi
            paying_students = random.randint(2, 6)
            for _ in range(paying_students):
                amount = monthly_fee
                data.append({
                    'date': date_str,
                    'amount': amount,
                    'description': f"O'quv kursi to'lovi (Sardor {random.randint(1,100)})",
                    'category': 'Daromad'
                })
        elif day_of_month > 10 and not is_weekend:
            # Kechikib to'laydiganlar (kamdan kam)
            if random.random() < 0.3:
                data.append({
                    'date': date_str,
                    'amount': monthly_fee,
                    'description': f"O'quv kursi to'lovi (kechikkan)",
                    'category': 'Daromad'
                })

        # 2. XARAJATLAR
        
        # Arenda (oyning 5-sanasida)
        if day_of_month == 5:
            data.append({
                'date': date_str,
                'amount': -rent_cost,
                'description': "Ofis Ijarasi (Rent)",
                'category': 'Xarajat'
            })
            
        # O'qituvchi oyligi (oyning 10-sanasida)
        if day_of_month == 10:
            # O'tgan oy taxminiy tushum 20 mln desak
            salary = 20000000 * teacher_share
            data.append({
                'date': date_str,
                'amount': -salary,
                'description': "O'qituvchi oyligi",
                'category': 'Xarajat'
            })
            
        # Kommunal (Svet, Gaz, Suv) - 2026 narxlar oshgan
        if day_of_month == 15:
            electr_cost = random.randint(400000, 600000) # Qish (Jan-Feb) konditsioner/isitish
            data.append({'date': date_str, 'amount': -electr_cost, 'description': "Elektr energiyasi", 'category': 'Kommunal'})
            
            data.append({'date': date_str, 'amount': -random.randint(50000, 100000), 'description': "Suv (Water)", 'category': 'Kommunal'})
            data.append({'date': date_str, 'amount': -random.randint(200000, 400000), 'description': "Isitish (Gaz/Otoplenie)", 'category': 'Kommunal'})

        # Internet (oyning 1-sanasida)
        if day_of_month == 1:
            data.append({'date': date_str, 'amount': -300000, 'description': "Internet (Optika)", 'category': 'Aloqa'})

        # Kichik xarajatlar (Suv idish, stakan, marker)
        if random.random() < 0.4 and not is_weekend:
            data.append({
                'date': date_str,
                'amount': -random.randint(50000, 150000),
                'description': "Ofis xarajatlari (Suv, qog'oz, marker)",
                'category': 'Xarajat'
            })
            
        # Kutilmagan buzilish (Computer repair)
        if random.random() < 0.05: # 5% ehtimol
            data.append({
                'date': date_str,
                'amount': -random.randint(200000, 1000000),
                'description': "Kompyuter ta'miri / Texnika",
                'category': 'Xarajat'
            })

        current_date += timedelta(days=1)
        
    return pd.DataFrame(data)

def generate_restaurant_data():
    """
    Kichik Milliy Taomlar Restorani (2026)
    - 10-12 stol
    - O'rtacha chek: 80,000 UZS
    - Kunlik tushum: 2-4 mln UZS
    - Xarajat: Bozorlik (Go'sht, Sabzavot), Xodimlar (kunlik/oylik), Arenda
    """
    start_date = datetime(2026, 1, 1)
    days = 60
    data = []
    
    # Arenda (Kattaroq joy): ~$1000 => ~13 mln UZS
    rent_cost = 13000000
    
    current_date = start_date
    for i in range(days):
        date_str = current_date.strftime('%Y-%m-%d')
        weekday = current_date.weekday() # 0=Mon, 6=Sun
        is_weekend = weekday >= 5 or weekday == 4 # Fri, Sat, Sun - zo'r savdo
        
        # 1. KUNLIK TUSHUM (Sales)
        # O'rtacha 10 stol x 4 oborot x 80k = 3.2 mln
        if is_weekend:
            daily_income = random.uniform(3500000, 5000000)
        else:
            daily_income = random.uniform(2000000, 3000000)
            
        # Tushum har xil tranzaksiyalar bilan tushadi (Click, Naqd, Payme) - biz yig'indisini yozamiz yoki bo'lib
        # Keling, bo'lib yozamiz
        data.append({
            'date': date_str, 
            'amount': daily_income * 0.4, 
            'description': "Tushum (Naqd)", 
            'category': 'Daromad'
        })
        data.append({
            'date': date_str, 
            'amount': daily_income * 0.6, 
            'description': "Tushum (Terminal/Click)", 
            'category': 'Daromad'
        })
        
        # 2. XARAJATLAR (Daily)
        
        # Bozorlik (Go'sht, Yog', Guruch, Sabzavot)
        # Odatda tushumning 40-50% i mahsulotga ketadi
        product_cost = daily_income * random.uniform(0.35, 0.45)
        
        # Go'sht (har kuni yoki 2 kunda 1)
        if i % 2 == 0:
            meat_cost = product_cost * 0.6 * 2 # 2 kunlik zaxira
            data.append({
                'date': date_str,
                'amount': -meat_cost,
                'description': "Go'sht mahsulotlari xaridi",
                'category': 'Bozorlik'
            })
        
        # Sabzavot va boshqalar (har kuni)
        veg_cost = product_cost * 0.4
        data.append({
            'date': date_str,
            'amount': -veg_cost,
            'description': "Sabzavot va boshqa masalliqlar",
            'category': 'Bozorlik'
        })
        
        # Xodimlar (Ofitsiant kunlik, Oshpaz oylik yoki kunlik)
        # Ofitsiantlar tushumdan % oladi (bonus), lekin fix oylik ham bo'lishi mumkin. 
        # Soddalashtiramiz: Kunlik to'lov (yoki xizmat haqi ularniki)
        # Faraz qilamiz: kunlik xarajat (daily wage)
        daily_wages = 300000 # 3-4 ishchi
        data.append({'date': date_str, 'amount': -daily_wages, 'description': "Xodimlar kunlik ish haqi", 'category': 'Xarajat'})
        
        # Arenda (oyning 5-sanasida)
        if current_date.day == 5:
            data.append({
                'date': date_str,
                'amount': -rent_cost,
                'description': "Restoran Ijarasi",
                'category': 'Xarajat'
            })
            
        # Soliq (oyning 15-sanasida) - Aylanmadan 4% (soddalashtirilgan)
        if current_date.day == 15:
            # Oyiga taxminan 100 mln tushum -> 4 mln soliq
            tax_cost = 4000000
            data.append({
                'date': date_str,
                'amount': -tax_cost,
                'description': "Soliq (Aylanmadan)",
                'category': 'Xarajat'
            })
            
        # Kommunal (Svet, Gaz kuchli ishlaydi restoranda)
        if current_date.day == 20:
            data.append({'date': date_str, 'amount': -1500000, 'description': "Elektr va Gaz", 'category': 'Kommunal'})

        current_date += timedelta(days=1)
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Ma'lumotlar generatsiya qilinmoqda...")
    
    # 1. O'quv markazi
    df_edu = generate_edu_center_data()
    df_edu.to_csv("edu_center_2026.csv", index=False)
    print(f"Edu Center: {len(df_edu)} ta tranzaksiya saqlandi (edu_center_2026.csv)")
    
    # 2. Restoran
    df_rest = generate_restaurant_data()
    df_rest.to_csv("restaurant_2026.csv", index=False)
    print(f"Restaurant: {len(df_rest)} ta tranzaksiya saqlandi (restaurant_2026.csv)")
