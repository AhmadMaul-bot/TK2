# Dataset: P1(0,5,2), P2(2,3,1), P3(3,10,4), P4(4,4,2), P5(7,6,3)
# Format: (Arrival Time, Burst Time, Priority) - Angka prioritas kecil = tinggi
processes = [
    {"id": "P1", "arrival": 0, "burst": 5, "priority": 2},
    {"id": "P2", "arrival": 2, "burst": 3, "priority": 1},
    {"id": "P3", "arrival": 3, "burst": 10, "priority": 4},
    {"id": "P4", "arrival": 4, "burst": 4, "priority": 2},
    {"id": "P5", "arrival": 7, "burst": 6, "priority": 3},
]

def simulate_fcfs(procs):
    print("\n--- FCFS ---")
    procs.sort(key=lambda x: x['arrival'])
    time, total_wt, total_tat, total_rt = 0, 0, 0, 0
    
    for p in procs:
        if time < p['arrival']: time = p['arrival']
        rt = time - p['arrival']
        time += p['burst']
        tat = time - p['arrival']
        wt = tat - p['burst']
        
        total_rt += rt; total_wt += wt; total_tat += tat
        print(f"{p['id']}: Response={rt}, Waiting={wt}, Turnaround={tat}")
        
    n = len(procs)
    print(f"Rata-rata: Response={total_rt/n:.2f}, Waiting={total_wt/n:.2f}, Turnaround={total_tat/n:.2f}")

def simulate_sjf_srtf(procs):
    print("\n--- SRTF (Preemptive SJF) ---")
    time, completed, n = 0, 0, len(procs)
    total_wt, total_tat, total_rt = 0, 0, 0
    
    for p in procs:
        p['rem'] = p['burst']
        p['start'] = -1

    while completed < n:
        idx, min_rem = -1, float('inf')
        for i in range(n):
            if procs[i]['arrival'] <= time and procs[i]['rem'] > 0 and procs[i]['rem'] < min_rem:
                min_rem = procs[i]['rem']
                idx = i
                
        if idx != -1:
            p = procs[idx]
            if p['start'] == -1: p['start'] = time
            p['rem'] -= 1
            time += 1
            if p['rem'] == 0:
                completed += 1
                tat = time - p['arrival']
                wt = tat - p['burst']
                rt = p['start'] - p['arrival']
                total_rt += rt; total_wt += wt; total_tat += tat
                print(f"{p['id']}: Response={rt}, Waiting={wt}, Turnaround={tat}")
        else:
            time += 1
            
    print(f"Rata-rata: Response={total_rt/n:.2f}, Waiting={total_wt/n:.2f}, Turnaround={total_tat/n:.2f}")

def simulate_priority(procs):
    print("\n--- Preemptive Priority Scheduling ---")
    time, completed, n = 0, 0, len(procs)
    total_wt, total_tat, total_rt = 0, 0, 0
    
    for p in procs:
        p['rem'] = p['burst']
        p['start'] = -1

    while completed < n:
        idx, min_prio = -1, float('inf')
        for i in range(n):
            if procs[i]['arrival'] <= time and procs[i]['rem'] > 0 and procs[i]['priority'] < min_prio:
                min_prio = procs[i]['priority']
                idx = i
                
        if idx != -1:
            p = procs[idx]
            if p['start'] == -1: p['start'] = time
            p['rem'] -= 1
            time += 1
            if p['rem'] == 0:
                completed += 1
                tat = time - p['arrival']
                wt = tat - p['burst']
                rt = p['start'] - p['arrival']
                total_rt += rt; total_wt += wt; total_tat += tat
                print(f"{p['id']}: Response={rt}, Waiting={wt}, Turnaround={tat}")
        else:
            time += 1
            
    print(f"Rata-rata: Response={total_rt/n:.2f}, Waiting={total_wt/n:.2f}, Turnaround={total_tat/n:.2f}")

def simulate_round_robin(procs, quantum):
    print(f"\n--- Round Robin (Quantum = {quantum}) ---")
    n = len(procs)
    for p in procs:
        p['rem'] = p['burst']
        p['start'] = -1
        
    procs.sort(key=lambda x: x['arrival'])
    time, completed, idx_tracker = 0, 0, 0
    queue = []
    total_wt, total_tat, total_rt = 0, 0, 0

    while idx_tracker < n and procs[idx_tracker]['arrival'] <= time:
        queue.append(procs[idx_tracker])
        idx_tracker += 1

    while completed < n:
        if not queue:
            time = procs[idx_tracker]['arrival']
            while idx_tracker < n and procs[idx_tracker]['arrival'] <= time:
                queue.append(procs[idx_tracker])
                idx_tracker += 1
                
        p = queue.pop(0)
        if p['start'] == -1: p['start'] = time
        
        run_time = min(p['rem'], quantum)
        time += run_time
        p['rem'] -= run_time
        
        while idx_tracker < n and procs[idx_tracker]['arrival'] <= time:
            queue.append(procs[idx_tracker])
            idx_tracker += 1
            
        if p['rem'] > 0:
            queue.append(p)
        else:
            completed += 1
            tat = time - p['arrival']
            wt = tat - p['burst']
            rt = p['start'] - p['arrival']
            total_rt += rt; total_wt += wt; total_tat += tat
            print(f"{p['id']}: Response={rt}, Waiting={wt}, Turnaround={tat}")

    print(f"Rata-rata: Response={total_rt/n:.2f}, Waiting={total_wt/n:.2f}, Turnaround={total_tat/n:.2f}")

if __name__ == "__main__":
    import copy
    simulate_fcfs(copy.deepcopy(processes))
    simulate_sjf_srtf(copy.deepcopy(processes))
    simulate_priority(copy.deepcopy(processes))
    simulate_round_robin(copy.deepcopy(processes), quantum=4)
    simulate_round_robin(copy.deepcopy(processes), quantum=6)