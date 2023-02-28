select t.`sell?` from ticket as t
                 join timetable as tt on tt.idTimetable = t.Timetable_idTimetable
                 where t.Timetable_idTimetable = '$tt_id';