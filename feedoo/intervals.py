def raw_window(min_value:int, max_value:int, interval:int):
    output = list()
    for window_start in range(min_value, max_value+1, interval):
        window_end = window_start + interval - 1
        output.append((window_start, window_end)) 
    
    return output

def clamped_window(min_value:int, max_value:int, interval:int):
    window = raw_window(min_value, max_value, interval)
    if window[-1][1] > max_value:
        window[-1] = (window[-1][0], max_value)
    
    return window

def intersect(i1_start:int, i1_end:int, i2_start:int, i2_end:int):
    # Hypothesis : i1_start <= i1_end, i2_start <= i2_end

    if i1_end < i2_start or i2_end < i1_start:
        return None, None
    else:
        return max(i1_start, i2_start), min(i1_end, i2_end)

def iterate_intervals(start_global:int, end_global:int, interval:int, segments:list, _func=clamped_window):
    output = list()
    for start_segment, end_segment in segments:
        start_tmp, end_tmp = intersect(start_global, end_global, start_segment, end_segment)
        if start_tmp is not None:
            output.append(_func(start_tmp, end_tmp, interval))
        else:
            output.append(None)

    return output