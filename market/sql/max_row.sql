select max(s.Line) from timetable as tt
                   join place as p on p.idPlace = tt.Place_idPlace
                   join seat as s on s.Place_idPlace = p.idPlace
                   where tt.idTimetable = '$tt_id';