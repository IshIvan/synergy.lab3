import csv
import datetime
import math


def main():
    def get_first_period():
        return [datetime.date(2012, 1, 1), datetime.date(2013, 1, 1)]

    def get_second_period():
        return [datetime.date(2002, 1, 1), datetime.date(2003, 1, 1)]

    def get_middle_value(array):
        sum = 0
        count = 0
        for item in array:
            sum += item[1]
            count += 1
        return sum / count

    def delta(array, mid_value):
        max_value = -100
        min_value = 100
        sum = 0
        quad_sum = 0
        for item in array:
            delt = item[1] - mid_value
            quad_sum += delt * delt
            sum += delt
            max_value = max(max_value, sum)
            min_value = min(min_value, sum)

        return [min_value, max_value, (quad_sum / len(array)) ** 0.5]

    def getH(array):
        mid_value = get_middle_value(array)
        delt = delta(array, mid_value)
        R = delt[1] - delt[0]
        S = delt[2]
        RS = R / S
        log10 = math.log(RS, 10)
        log_npi = math.log(len(array) * math.pi / 2, 10)
        return log10 / log_npi

    def print_header(period, data):
        print()
        print('с {0} по {1} наш супер биткоин имел показатель Херста:'
              .format(period[0].strftime('%d.%m.%Y'), period[1].strftime('%d.%m.%Y')))
        print(data)

    with open('gbp_quotes.csv', newline='') as f:
        reader = csv.reader(f)
        first_period_array = []
        second_period_array = []
        for row in reader:
            try:
                dict = row[0].split(';')
                price = dict[1]
                unix_date = datetime.datetime.strptime(dict[0], '%Y-%m-%d').date()
                period = get_first_period()
                if period[0] <= unix_date < period[1]:
                    first_period_array.append([unix_date, float(price)])

                period = get_second_period()
                if period[0] <= unix_date < period[1]:
                    second_period_array.append([unix_date, float(price)])
            except IndexError:
                print('out of')
            except Exception as e:
                print(e)
                continue

        print_header(get_first_period(), getH(first_period_array))
        print_header(get_second_period(), getH(second_period_array))


if __name__ == '__main__':
    main()
