select f.Country, sum(t.total_price) from timetable as tt
                                     join film as f on f.idFilm = tt.Film_idFilm
                                     join ticket as t on t.Timetable_idTimetable = tt.idTimetable
                                     where (to_days(now()) - to_days(tt.Date_show)) <=30
                                     and t.`sell?`=1
                                     group by tt.Film_idFilm;
