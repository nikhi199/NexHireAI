CREATE DATABASE NexHireAI;

use NexHireAI

CREATE TABLE Users (
   user_id INT primary key Identity(1,1),
   name VARCHAR(100),
   email VARCHAR(100),
   password Varchar (100),
   skills VARCHAR(200)
   );


   CREATE TABLE jobs(
    job_id INT PRIMARY KEY IDENTITY(1,1),
    title VARCHAR(100),
    location VARCHAR(200),
    Skill_required VARCHAR(300)
    );


    select * from users
    select * from jobs