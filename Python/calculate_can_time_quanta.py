import argparse

def calculate_can_timing(can_clock, bit_rate, sample_point_percent):
    total_tq = can_clock // bit_rate
    sync_seg = 1

    sample_point_tq = int(total_tq * sample_point_percent / 100)
    prop_seg_plus_seg1 = sample_point_tq - sync_seg

    prop_seg = prop_seg_plus_seg1 // 2
    seg1 = prop_seg_plus_seg1 - prop_seg
    seg2 = total_tq - sample_point_tq

    brp = can_clock // (bit_rate * total_tq)

    return {
        "Sync_Seg": sync_seg,
        "Prop_Seg": prop_seg,
        "Phase_Seg1": seg1,
        "Phase_Seg2": seg2,
        "BRP": brp,
        "Total_TQ": total_tq
    }

def main():
    parser = argparse.ArgumentParser(description="Calculate CAN timing parameters.")
    parser.add_argument("can_clock", type=int, help="CAN clock frequency in Hz")
    parser.add_argument("bit_rate", type=int, help="Desired CAN bit rate in bps")
    parser.add_argument("sample_point", type=float, help="Sample point percentage (e.g., 87.5)")

    args = parser.parse_args()
    timing = calculate_can_timing(args.can_clock, args.bit_rate, args.sample_point)

    print("Calculated CAN Timing Parameters:")
    for key, value in timing.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    main()
