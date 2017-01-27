import os


class StopTime:
    def __init__(self, line=""):
        split_line = line.split(",")
        self.trip_id = split_line[0]
        self.stop_sequence = int(split_line[1])
        self.stop_id = split_line[2]
        self.departure_time = split_line[5]
        self.pickup_type = split_line[6]
        self.drop_off_type = split_line[7]
        self.timePoint = split_line[8]
        self.shape_dist_traveled = float(split_line[9])
        self.prev_stop_id = self.stop_id
        self.prev_departure_time = self.departure_time
        self.distance_from_previous = self.shape_dist_traveled

    def __str__(self):
        return "{},{},{},{},{},{},{},{},{},{}".format(self.stop_sequence, self.stop_id, self.departure_time,
                                                      self.pickup_type, self.drop_off_type, self.timePoint,
                                                      self.shape_dist_traveled, self.prev_stop_id,
                                                      self.prev_departure_time, self.distance_from_previous)

    @staticmethod
    def get_header():
        return "stop_sequence,stop_id,departure_time,pickup_type,drop_off_type,timePoint,shape_dist_traveled," \
               "prev_stop_id,prev_departure_time,distance_from_previous"

    def add_fields_from_previous(self, prev):
        self.prev_stop_id = prev.stop_id
        self.prev_departure_time = prev.departure_time
        self.distance_from_previous = self.shape_dist_traveled - prev.shape_dist_traveled


class StopTimeCollection:
    @staticmethod
    def delete_file_if_exists(file):
        try:
            os.remove(file)
        except OSError:
            pass

    def __init__(self, destination_file):
        self.stopTimeGroup = []
        self.destinationFile = destination_file
        StopTimeCollection.delete_file_if_exists(destination_file)

        with open(self.destinationFile, "a+") as f:
            f.write("{0}\n".format(StopTime.get_header()))

    def order_stop_time_group(self):
        self.stopTimeGroup.sort(key=lambda s: s.stop_sequence)

    def set_extra_stop_time_fields(self):

        for index in range(1, len(self.stopTimeGroup)):
            self.stopTimeGroup[index].add_fields_from_previous(self.stopTimeGroup[index - 1])

    def process_stop_time_line(self, line):
        stop_time = StopTime(line)
        if len(self.stopTimeGroup) == 0:
            self.stopTimeGroup.append(stop_time)
            return

        if stop_time.trip_id == self.stopTimeGroup[-1].trip_id:
            self.stopTimeGroup.append(stop_time)
        else:
            self.order_stop_time_group()
            self.set_extra_stop_time_fields()
            self.save_group_to_file()
            self.stopTimeGroup.clear()

    def save_group_to_file(self):
        with open(self.destinationFile, "a+") as f:
            for stop_time in self.stopTimeGroup:
                f.write("{0}\n".format(str(stop_time)))


def read_csv(input_file, process_line):
    with open(input_file) as f:
        next(f)
        for line in f:
            process_line(line)


inputFile = r'D:\Personale\TensorExamples\tensorflow\small_stop_times.csv'
processedFile = r'D:\Personale\TensorExamples\tensorflow\stop_times_proc.csv'

if __name__ == '__main__':
    stopTimeCollection = StopTimeCollection(processedFile)
    read_csv(inputFile, stopTimeCollection.process_stop_time_line)
