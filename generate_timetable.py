from ortools.sat.python import cp_model
import pandas as pd
from collections import defaultdict

def generate_timetable(csv_path):
    try:
        df = pd.read_csv(csv_path)
        teachers = df['Teacher'].unique().tolist()
        sections = df['Section'].unique().tolist()
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']
        slots_per_day = 6
        total_slots = len(days) * slots_per_day

        model = cp_model.CpModel()
        variables = {}

        for i, row in df.iterrows():
            for slot in range(total_slots):
                variables[(i, slot)] = model.NewBoolVar(f'lec_{i}_slot{slot}')

        for i, row in df.iterrows():
            model.Add(sum(variables[(i, slot)] for slot in range(total_slots)) == int(row['Hours']))

        for teacher in teachers:
            for slot in range(total_slots):
                model.Add(
                    sum(variables[(i, slot)] for i, row in df.iterrows() if row['Teacher'] == teacher) <= 1
                )

        for section in sections:
            for slot in range(total_slots):
                model.Add(
                    sum(variables[(i, slot)] for i, row in df.iterrows() if row['Section'] == section) <= 1
                )

        # Prevent consecutive slots for same teacher
        for teacher in teachers:
            for day in range(len(days)):
                for p in range(slots_per_day - 1):
                    slot1 = day * slots_per_day + p
                    slot2 = slot1 + 1
                    model.Add(
                        sum(variables[(i, slot1)] + variables[(i, slot2)]
                            for i, row in df.iterrows() if row['Teacher'] == teacher) <= 1
                    )

        # Prevent consecutive slots for same section
        for section in sections:
            for day in range(len(days)):
                for p in range(slots_per_day - 1):
                    slot1 = day * slots_per_day + p
                    slot2 = slot1 + 1
                    model.Add(
                        sum(variables[(i, slot1)] + variables[(i, slot2)]
                            for i, row in df.iterrows() if row['Section'] == section) <= 1
                    )

        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            timetable = defaultdict(lambda: [['' for _ in range(slots_per_day)] for _ in range(len(days))])

            for i, row in df.iterrows():
                for slot in range(total_slots):
                    if solver.Value(variables[(i, slot)]):
                        day_idx = slot // slots_per_day
                        period_idx = slot % slots_per_day
                        cell = f"{row['Subject']} ({row['Teacher']})"
                        timetable[row['Section']][day_idx][period_idx] = cell

            return {
                'sections': sections,
                'days': days,
                'slots_per_day': slots_per_day,
                'timetable': timetable
            }
        else:
            return None
    except Exception as e:
        print("Error generating timetable:", e)
        return None
