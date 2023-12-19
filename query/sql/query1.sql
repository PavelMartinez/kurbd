select f.Title, sum(t.total_price) from timetable as tt
                                     join film as f on f.idFilm = tt.Film_idFilm
                                     join ticket as t on t.Timetable_idTimetable = tt.idTimetable
                                     where year(tt.Date_show) = '$input_year'
                                     and month(tt.Date_show) = '$input_month'
                                     and t.`sell?`=1
                                     group by tt.Film_idFilm;
