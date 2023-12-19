select t.idTicket from ticket as t
                  join timetable as tt on tt.idTimetable = t.Timetable_idTimetable
                  where t.Timetable_idTimetable = '$tt_id' and t.Line_s = '$line_id' and t.Number_s = '$number_id';