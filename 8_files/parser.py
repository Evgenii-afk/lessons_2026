class Info:
    def __init__(self, ip, day, response_code, size, user_agent):
        self.ip = ip
        self.day = day
        self.response_code = response_code
        self.size = size
        self.user_agent = user_agent

infos = []

#ip - - date request response_code size - user_agent
#93.180.71.3 - - [17/May/2015:08:05:32 +0000] "GET /downloads/product_1 HTTP/1.1" 304 0 "-" "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"
with open("access_log", "r") as file:
    for line in file:
        ip = line.split(" ")[0]
        date_full = line.split("[")[-1].split("]")[0]
        day = date_full.split(":")[0]
        request = line.split("\"")[1]
        response_code = line.split("\"")[2].split(" ")[1]
        size = line.split("\"")[2].split(" ")[2]
        user_agent = line.split("\"")[-2]
        
        infos.append(Info(ip, day, int(response_code), int(size), user_agent))

users_agents_counter = {}
for info in infos:
    if info.user_agent not in users_agents_counter:
        users_agents_counter[info.user_agent] = 0
    users_agents_counter[info.user_agent] += 1

users_agents_sorted = sorted(users_agents_counter.items(), key=lambda x: x[1], reverse=True)
print("10 user_agent")
for i in range(min(10, len(users_agents_sorted))):
    print(users_agents_sorted[i])

traffic_by_ip_day = {}

for info in infos:
    if info.ip not in traffic_by_ip_day:
        traffic_by_ip_day[info.ip] = {}
    
    if info.day not in traffic_by_ip_day[info.ip]:
        traffic_by_ip_day[info.ip][info.day] = 0
    
    traffic_by_ip_day[info.ip][info.day] += info.size

peak_traffic = {}
for ip, days in traffic_by_ip_day.items():
    peak_traffic[ip] = max(days.values())

peak_sorted = sorted(peak_traffic.items(), key=lambda x: x[1], reverse=True)

print("10 IP по пиковому суточному трафику:")
for i in range(min(10, len(peak_sorted))):
    print(f"IP: {peak_sorted[i][0]}, пиковый трафик: {peak_sorted[i][1]} байт")