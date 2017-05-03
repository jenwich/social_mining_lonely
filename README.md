## Requirements

* python3
* tweepy
* pymongo

## Setup

* Install packages

  ```sh
  pip install -r requirements.txt
  ```

* Copy `secret.py` and change keys

## Run

* Collect user following

  ```sh
  python get_following.py <FROM> <TO>
  ```
   
* Calculate mutual friends (friend coeff)

  ```sh
  python friend_coeff.py <FROM> <TO>
  ```
* Export database

  ```sh
  python export_database.py COLLECTION
  ```

  COLLECTION = tweet | user | friend_coeff
 
## Files detail

* `get_data.py` - ดึง search tweet ลง database (อันนี้ไม่ต้องรันแล้ว)
* `get_user.py` - ดึงข้อมูล user จาก tweet ใน database แล้วเก็บเป็น collection ใหม่ (ห้ามรัน เดี๋ยวข้อมูลมันทับของเดิม)
* `get_following.py` - ดึงข้อมูล following ของ user ใส่ใน collection user
* `friend_coeff.py` - คำนวณ mutual friends แล้วเก็บลง database
* `count_tweet.py` - ดึงชื่อและจำนวน tweet ของ user แต่ละคน
* `export_database.py` - export แต่ละ collection เป็น json file
* `keywords.txt` - เก็บ keyword ที่จะ search
* `secret.py` - เก็บ key ต่างๆ กับ parameter ของ database

