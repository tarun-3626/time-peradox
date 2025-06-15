from collections import defaultdict

# Detect scheduling conflicts
def detect_conflicts(timetable):
    conflicts = []
    for section, days in timetable.items():
        for day, sessions in days.items():
            hour_map = defaultdict(list)
            for subject, teacher, hour in sessions:
                hour_map[hour].append((subject, teacher))
            for hour, entries in hour_map.items():
                if len(entries) > 1:
                    conflicts.append((section, day, hour, entries))
    return conflicts

# Count how many hours each teacher is teaching
def teacher_load(timetable):
    load = defaultdict(int)
    for section, days in timetable.items():
        for day, sessions in days.items():
            for subject, teacher, hour in sessions:
                load[teacher] += 1
    return dict(load)

# Find free hours for each section
def find_free_hours(timetable, start_hour=9, end_hour=17):
    free_slots = defaultdict(lambda: defaultdict(list))  # section -> day -> free hours
    full_hours = [str(h) for h in range(start_hour, end_hour + 1)]

    for section, days in timetable.items():
        for day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            scheduled = [hour for _, _, hour in days.get(day, [])]
            free = [h for h in full_hours if h not in scheduled]
            free_slots[section][day] = free
    return free_slots

# Pretty print conflicts
def print_conflicts(conflicts):
    if not conflicts:
        print("✅ No conflicts found.")
        return
    print("\n⚠️ Conflicts Detected:")
    for section, day, hour, entries in conflicts:
        print(f"Section {section} - {day} at {h
