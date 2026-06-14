CREATE DATABASE NexHireAI;

use NexHireAI

CREATE TABLE Users (
   user_id INT primary key Identity(1,1),
   name VARCHAR(100),
   email VARCHAR(100) unique,
   password Varchar (100),
   skills VARCHAR(200)
   );


   CREATE TABLE Jobs
   (
   job_id INT PRIMARY KEY IDENTITY(1,1),

   title VARCHAR(100),
   company Varchar(199),
   location Varchar (199),
   skills_required Varchar(500),
   Salary Varchar(50),
   Description Varchar(Max),

   posted_date DATETIME DEFAULT GETDATE()
   );



    ALTER TABLE USERS
    ADD Education varchar(199),
        Experience varchar (199),
        Resumepath Varchar(199);

        


   CREATE TABLE Applications(

    application_id INT PRIMARY KEY IDENTITY(1,1),

    user_id INT,

    job_id INT,

    apply_date DATETIME DEFAULT GETDATE(),

    status VARCHAR(50) DEFAULT 'Pending',

    FOREIGN KEY(user_id) REFERENCES Users(user_id),

    FOREIGN KEY(job_id) REFERENCES Jobs(job_id)
    );


    EXEC sp_rename
'Jobs.Deascription',
'description',
'COLUMN';

    select * from users
    select * from jobs
    select * from Applications

    SELECT title,
       company,
       location,
       skills_required,
       salary,
       description
FROM Jobs;

SELECT
name,
skills,
Education,
Experience
FROM Users;