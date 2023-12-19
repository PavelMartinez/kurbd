select f.Title, p.Place_name, tt.idTimetable from timetable as tt
                                          join film as f on f.idFilm = tt.Film_idFilm
                                          join place as p on p.idPlace = tt.Place_idPlace
                                          where tt.Date_show = '$date_id';