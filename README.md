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
 
## Files detail

* `get_data.py` - ดึง search tweet ลง database (อันนี้ไม่ต้องรันแล้ว)
* `get_user.py` - ดึงข้อมูล user จาก tweet ใน database แล้วเก็บเป็น collection ใหม่ (ห้ามรัน เดี๋ยวข้อมูลมันทับของเดิม)
* `get_following.py` - ดึงข้อมูล following ของ user ใส่ใน collection user
* `keywords.txt` - เก็บ keyword ที่จะ search
* `secret.py` - เก็บ key ต่างๆ กับ parameter ของ database

