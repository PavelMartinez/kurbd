select t.total_price from timetable as tt
                   join ticket as t on t.Timetable_idTimetable = tt.idTimetable
                   where tt.idTimetable = '$tt_id'
                   order by t.total_price desc;