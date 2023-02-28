select f.Country, count(t.`sell?`) from timetable as tt
                                     join film as f on f.idFilm = tt.Film_idFilm
                                     join ticket as t on t.Timetable_idTimetable = tt.idTimetable
                                     where year(tt.Date_show) = '$input_year'
                                     group by tt.Film_idFilm
                                     order by count(t.`sell?`) Desc;