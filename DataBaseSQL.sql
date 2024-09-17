CREATE TABLE IF NOT EXISTS userinfor (
    userid SERIAL PRIMARY KEY, 
    username VARCHAR(255) NOT NULL,
    groupid INT
);

CREATE TABLE IF NOT EXISTS groupinfo (
    groupid SERIAL PRIMARY KEY,  
    groupname VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS alltask (
    taskid SERIAL PRIMARY KEY,                     
    userid INT,                                    
    groupid INT,                                  
    taskname VARCHAR(255) NOT NULL,
    date DATE,
    FOREIGN KEY (userid) REFERENCES userinfor(userid),
    FOREIGN KEY (groupid) REFERENCES groupinfo(groupid)
);


