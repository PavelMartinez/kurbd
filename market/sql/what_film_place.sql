select f.Title, f.idFilm, p.idPlace, p.Place_name from timetable as tt
                                                    join film as f on f.idFilm = tt.Film_idFilm
                                                    join place as p on p.idPlace = tt.Place_idPlace
                                                    where tt.idTimetable = '$tt_id';