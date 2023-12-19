SELECT tt.Place_idPlace, p.Place_name, COUNT(*) FROM timetable as tt
JOIN place as p ON p.idPlace = tt.Place_idPlace
WHERE (MONTH(tt.Date_show) = '$input_month' AND YEAR(tt.Date_show)='$input_year')
GROUP BY tt.Place_idPlace;
