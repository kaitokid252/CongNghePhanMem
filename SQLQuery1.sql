CREATE DATABASE QuanLyNhaHang
GO

USE QuanLyNhaHang
GO

-- Food
-- Table
-- FoodCategory
-- Account
-- Bill
-- BillInfo

CREATE TABLE TableFood
(
	id INT IDENTITY PRIMARY KEY,
	name NVARCHAR(100)  NOT NULL,
	status INT NOT NULL	-- 1 Co nguoi || 0 trong	
)
GO

CREATE TABLE Account
(
	UserName NVARCHAR(100) PRIMARY KEY NOT NULL,	
	PassWord NVARCHAR(1000) NOT NULL ,
)
GO
CREATE TABLE Food
(
	id INT PRIMARY KEY,
	name NVARCHAR(100) NOT NULL,
	price INT NOT NULL,
	count INT DEFAULT 0 NOT NULL,
)
GO
CREATE TABLE Bill
(
	id INT IDENTITY PRIMARY KEY,
	idTable INT NOT NULL,
	CheckIn DATE NOT NULL,
	Checkout DATE,
	Totalprice INT NOT NULL DEFAULT 0,
	status INT NOT NULL,
	FOREIGN KEY (idTable) REFERENCES dbo.TableFood(id)
)
Go
CREATE TABLE OrderFood
(
idTable INT NOT NULL,
idFood INT NOT NULL,
FOREIGN KEY (idTable) REFERENCES dbo.TableFood(id),
FOREIGN KEY (idFood) REFERENCES dbo.Food(id)
)
GO
INSERT dbo.Food
(
    id,
    name,
    price,
    count
)
VALUES
(   2,   -- id - int
    N'Gà', -- name - nvarchar(100)
    300000,   -- price - int
    1    -- count - int
    )
INSERT dbo.TableFood
(
    name,
    status
)
VALUES
(   N'', -- name - nvarchar(100)
    0    -- status - int
    )

INSERT dbo.Account
(
    UserName,
    PassWord
)
VALUES
(   N'K', -- UserName - nvarchar(100)
    N'1'  -- PassWord - nvarchar(1000)
    )

SELECT * FROM dbo.Account
SELECT * FROM dbo.TableFood
SELECT * FROM dbo.Food
SELECT * FROM dbo.Bill
DELETE FROM dbo.Bill


