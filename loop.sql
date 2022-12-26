-- select * from fuels;

DO $$
DECLARE
    fuel CHAR(50);
	id INT;
BEGIN
	id := 100;
    fuel := 'fuel';
    FOR counter IN 1..5
        LOOP
		   INSERT INTO fuels(fuel_id, fuel_name) 
		   VALUES (id + counter, fuel || counter || 'new');
        END LOOP;
END;
$$