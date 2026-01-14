import contextlib
import can


def calc(f_clock:int, nom_bitrate:int, data_bitrate:int):
    timings = set()
    for nominal_sample_point in range(75, 91):
        for data_sample_point in range(50, 91):
            with contextlib.suppress(ValueError):
             timings.add(
                 can.BitTimingFd.from_sample_point(
                     f_clock=f_clock,
                     nom_bitrate=nom_bitrate,
                     nom_sample_point=nominal_sample_point,
                     data_bitrate=data_bitrate,
                     data_sample_point=data_sample_point
                 )
             )

    for timing in sorted(timings, key=lambda x: x.nom_sample_point):
        if timing.data_bitrate % 10_000 == 0:
            print(timing)


def main():
    for f_clock in [25_000_000]:
        for nom_bitrate in [250_000, 500_000, 1_000_000]:
            if nom_bitrate < 1_000_000:
                data_bitrate = nom_bitrate
                calc(f_clock=f_clock, nom_bitrate=nom_bitrate, data_bitrate=data_bitrate)
            else:
                for data_bitrate in range(1_000_000, 5_500_000, 10_000):
                    calc(f_clock=f_clock, nom_bitrate=nom_bitrate, data_bitrate=data_bitrate)

if __name__ == "__main__":
    main()
