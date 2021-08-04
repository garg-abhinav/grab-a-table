CREATE TABLE Menu (
    food_item_id INT,
    food_item_desc TEXT,
    cuisine VARCHAR(20),
    food_type VARCHAR(20),
    image_url TEXT,
    base_price FLOAT(2),
    availability INT,
    prep_instructions TEXT,
    PRIMARY KEY(food_item_id)
);

CREATE TABLE Ingredients (
    ingredient_id INT,
    ingredient_desc VARCHAR(200),
    PRIMARY KEY(ingredient_id)
);

CREATE TABLE Recipe (
    food_item_id INT,
    ingredient_id INT,
    ingredient_quantity REAL,
    PRIMARY KEY(food_item_id, ingredient_id),
    FOREIGN KEY (food_item_id) REFERENCES Menu(food_item_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

CREATE TABLE Inventory (
    last_update_timestamp DATETIME,
    ingredient_id INT,
    qty REAL,
    PRIMARY KEY (last_update_timestamp, ingredient_id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredients(ingredient_id)
);

CREATE TABLE Promotions (
    promo_code VARCHAR(10),
    promo_desc TEXT,
    discount_percent INT,
    active INT,
    start_time DATETIME,
    end_time DATETIME,
    PRIMARY KEY (promo_code)
);

CREATE TABLE PaymentMethod (
    payment_method VARCHAR(50),
    payment_desc VARCHAR(100),
    PRIMARY KEY (payment_method)
);

CREATE TABLE Diners (
  mobile_number INT,
  customer_name VARCHAR(100),
  PRIMARY KEY (mobile_number)
);

CREATE TABLE Orders (
  order_id INT,
  order_placed_at DATETIME,
  order_completed_at DATETIME,
  order_status VARCHAR(20),
  mobile_number INT,
  total_billed_amount REAL,
  rating INT,
  feedback TEXT,
  transaction_id VARCHAR(30),
  payment_method VARCHAR(50),
  promo_code VARCHAR(10),
  net_payable REAL,
  PRIMARY KEY (order_id),
  FOREIGN KEY (mobile_number) REFERENCES Diners(mobile_number),
  FOREIGN KEY (payment_method) REFERENCES PaymentMethod(payment_method),
  FOREIGN KEY (promo_code) REFERENCES Promotions(promo_code)
);

CREATE TABLE Cart (
    food_item_id INT,
    order_id INT,
    qty INT,
    PRIMARY KEY (food_item_id, order_id),
    FOREIGN KEY (food_item_id) REFERENCES Menu(food_item_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);

-- Stored Procedure to update cart, inventory and return food price

DELIMITER //
DROP PROCEDURE IF EXISTS InventoryUpdate;
CREATE PROCEDURE InventoryUpdate(IN order_id INT
								,IN item_id INT
                                ,IN QTY INT
                                ,OUT ITEM_AMOUNT DOUBLE)
    label: BEGIN
          -- Declare all variables
		  DECLARE done BOOLEAN DEFAULT FALSE;
          DECLARE curr_ingredient_id INT;
          DECLARE ingredientcur CURSOR FOR SELECT DISTINCT ingredient_id FROM Recipe WHERE food_item_id=item_id;
          DECLARE CONTINUE HANDLER FOR NOT FOUND SET done=TRUE;
		  -- Update Inventory
		  DROP TABLE IF EXISTS INGREDIENT_QTY_TEMP;
          CREATE TABLE INGREDIENT_QTY_TEMP LIKE Recipe;
          INSERT INTO INGREDIENT_QTY_TEMP
          SELECT DISTINCT
                 A.food_item_id,
				 A.ingredient_id
                ,(A.ingredient_quantity*QTY) AS INGREDIENT_QTY_REQ
          FROM Recipe A
          WHERE A.food_item_id=item_id;
          OPEN ingredientcur;
          loop1: LOOP
				FETCH ingredientcur INTO curr_ingredient_id;
				IF curr_ingredient_id = NULL THEN
				    LEAVE loop1;
				END IF;
				IF done THEN
				    LEAVE loop1;
				END IF;
                INSERT INTO Inventory
                (SELECT DISTINCT
						 current_timestamp() AS Last_update_timestamp
						,A.ingredient_id
                        ,(B.qty_available-A.ingredient_quantity) AS QTY_AVAILABLE
                FROM INGREDIENT_QTY_TEMP A
                INNER JOIN (SELECT ingredient_id,qty_available
							FROM Inventory
                            WHERE last_update_timestamp IN (SELECT MAX(last_update_timestamp)
															FROM Inventory
                                                            WHERE Inventory.ingredient_id=curr_ingredient_id)
                                                            AND Inventory.ingredient_id=curr_ingredient_id) B ON A.ingredient_id=B.ingredient_id);
            END LOOP loop1;
            close ingredientcur;
            -- Inventory Updated
            -- Update Order ID -- Other columns should be nullable
            -- INSERT INTO Orders(order_id)
            -- VALUES (order_id);
            -- Order id updated
            -- Update Cart Table
             INSERT INTO Cart
             VALUES (item_id,order_id,QTY);
             -- Cart Updated
            -- Return amount
            SELECT A.base_price*QTY as ITEM_AMOUNT
            FROM Menu A
            WHERE A.food_item_id=item_id;
    END label
DELIMITER ;


-- This trigger executes when an insert is made in the orders table >>
-- Trigger for promotion code and discount >>
DELIMITER //
CREATE TRIGGER SaleTrig
    AFTER INSERT ON Orders
    FOR EACH ROW
  label: BEGIN
		-- Promo code variable
        SET @x=(SELECT DISTINCT PROMO_CODE
                FROM PROMOTIONS A
                WHERE new.ORDER_PLACED_AT BETWEEN A.START_TIME AND A.END_TIME
                AND A.ACTIVE=1),
        -- Discount % variable
		@y=(SELECT DISTINCT discount_percent
				FROM PROMOTIONS A
                WHERE new.ORDER_PLACED_AT BETWEEN A.START_TIME AND A.END_TIME
                AND A.ACTIVE=1);
       -- If bill amount is not null then replace row with promo code and net payable
       IF new.TOTAL_BILLED_AMOUNT IS NOT NULL THEN
            REPLACE INTO Orders (order_id,order_placed_at,order_completed_at,order_status,mobile_number,total_billed_amount,
          rating,feedback,transaction_id,payment_method,promo_code,net_payable)
          VALUES (new.order_id,new.order_placed_at,new.order_completed_at,new.order_status,new.mobile_number,new.total_billed_amount,
				  new.rating,feedback,new.transaction_id,new.payment_method,@x,(total_billed_amount*(100-@y)/100));
        END IF;
  END label
DELIMITER ;

-- Stored Procedure to update cart, inventory and return food price >>
DELIMITER //
DROP PROCEDURE IF EXISTS OrderUpdate;
CREATE PROCEDURE OrderUpdate(
             IN order_id INT
            ,IN ORDER_PLACED_AT DATETIME
            ,IN ORDER_COMPLETED_AT DATETIME
            ,IN ORDER_STATUS VARCHAR(50)
            ,IN MOBILE_NUMBER INT
            ,IN TOTAL_BILLED_AMOUNT DOUBLE
            ,IN RATING INT
            ,IN FEEDBACK TEXT
            ,IN TRANSACTION_ID VARCHAR(30)
            ,IN PAYMENT_METHOD VARCHAR(50))
    label: BEGIN
          REPLACE INTO Orders (order_id,order_placed_at,order_completed_at,order_status,mobile_number,total_billed_amount,
          rating,feedback,transaction_id,payment_method)
          VALUES (order_id,ORDER_PLACED_AT,ORDER_COMPLETED_AT,ORDER_STATUS,MOBILE_NUMBER,TOTAL_BILLED_AMOUNT,
				  RATING,FEEDBACK,TRANSACTION_ID,PAYMENT_METHOD);
    END label
DELIMITER ;

-- Advance Queries >>>>>>

-- Top 10 selling Food items in the restaurant since 2020
-- Offers can be added on these items or preparation time and cost for these can be reduced to increase profit
CREATE VIEW top_food_items AS SELECT
		 RM.food_item_ID
        ,RM.food_item_desc
        ,RM.Cuisine
        ,SUM(RC.qty) AS ITEM_QTY

FROM Restaurant.Orders RO
INNER JOIN Restaurant.Cart RC ON RO.order_id=RC.order_id
INNER JOIN Restaurant.Menu RM ON RM.food_item_id=RC.food_item_id
WHERE YEAR(RO.ORDER_PLACED_AT)>=2020
GROUP BY
		 1,2,3
ORDER BY ITEM_QTY DESC
LIMIT 10;



-- Most frequent food items in orders which had a rating of less than 3
-- Deep dives should be performed to understand whether a particular food item is leading to poor order ratings
-- Enchiladas with Mushroom Sauce was present in 380 of the low rating orders
CREATE VIEW low_ratings AS SELECT
		 RM.food_item_ID
        ,RM.food_item_desc
        ,COUNT(DISTINCT RO.ORDER_ID) AS LOW_RATING_ORDER_COUNT
FROM Restaurant.Orders RO
INNER JOIN Restaurant.Cart RC ON RO.order_id=RC.order_id
INNER JOIN Restaurant.Menu RM ON RM.food_item_id=RC.food_item_id
WHERE RO.RATING<=3
GROUP BY 1,2
ORDER BY COUNT(DISTINCT RO.ORDER_ID) DESC;

-- Hour and Day wise order count.
-- Staff can be ramped up during peak hours or peak days

CREATE VIEW active_days_hours AS SELECT
		 TYPE
		,METRIC_VALUE
        ,ORDER_COUNT
FROM (SELECT
		  'Hour' AS TYPE
		  ,CAST(HOUR(RO.ORDER_PLACED_AT) AS CHAR) AS METRIC_VALUE
          ,COUNT(RO.ORDER_ID) AS ORDER_COUNT
FROM Restaurant.Orders RO
GROUP BY 1,2
UNION ALL
SELECT
      'Weekday' AS TYPE
      ,DAYNAME(RO.ORDER_PLACED_AT) AS METRIC_VALUE
      ,COUNT(RO.ORDER_ID) AS ORDER_COUNT
FROM Restaurant.Orders RO
GROUP BY 1,2
) A
ORDER BY TYPE ASC,ORDER_COUNT DESC;