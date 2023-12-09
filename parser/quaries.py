SQL_UPDATE = """
                 UPDATE 
                    food_positions
                 SET 
                    dish_type = %s,
                    dish_details = %s, 
                    dish_grams = %s, 
                    dish_price = %s, 
                    dish_image = %s
                 WHERE 
                    dish_name = %s;
                 """

SQL_INSERT = """
                INSERT INTO 
                    food_positions (dish_type, 
                                    dish_name, 
                                    dish_details, 
                                    dish_grams, 
                                    dish_price, 
                                    dish_image)
                VALUES 
                    (%s, %s, %s, %s, %s, %s);
             """

