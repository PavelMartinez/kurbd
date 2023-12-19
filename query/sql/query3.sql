SELECT tt.idTimetable, tt.Date_show, f.Title
FROM timetable as tt
LEFT JOIN ticket as t ON t.Timetable_idTimetable = tt.idTimetable
JOIN film as f ON f.idFilm = tt.Film_idFilm
WHERE t.idTicket IS NULL AND YEAR(tt.Date_show) = '$input_year';
