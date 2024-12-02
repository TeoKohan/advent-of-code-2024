import re

with open('input') as input:
    reports = input.read().splitlines()
    reports = [[*map(int, re.findall(r'(\d+)', report))] for report in reports]

def safe_report(report: list[int]):
    pairwise_safe = all(1 <= abs(x-y) <= 3 for x, y in zip(report, report[1:]))
    monotone = report in [sorted(report), sorted(report, reverse=True)]
    return pairwise_safe and monotone

def count_safe_reports(reports: list[list[int]]) -> int:
    return sum([safe_report(report) for report in reports])

def count_safe_reports_with_dampener(reports: list[list[int]]) -> int:
    def derivations(report: list[int]) -> list[list[int]]:
        return [report] + [report[:i] + report[i+1:] for i in range(len(report))]
    return sum([any(safe_report(derived_report) for derived_report in derivations(report)) for report in reports])

with open('output', 'w') as output:
    output.write( str(count_safe_reports(reports)) + '\n')
    output.write( str(count_safe_reports_with_dampener(reports)) + '\n')