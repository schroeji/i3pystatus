from i3pystatus.core.command import run_through_shell
from i3pystatus import IntervalModule, formatp


class amdtemp(IntervalModule):

    settings = (
        ("format", "Format string below first threshold"),
        ("color0", "Color below first threshold"),
        ("color1", "Color above first threshold"),
        ("color2", "Color above second threshold"),
        ("threshold1", "First threshold for color values"),
        ("threshold2", "Second threshold for color values"),
    )
    interval = 5
    color0 = "#E7BA3C"
    color1 = "#E9853A"
    color2 = "#EC4E39"
    threshold1 = 55
    threshold2 = 65
        
    on_upscroll = "increase_fanspeed"
    on_downscroll = "reduce_fanspeed"

    format = "CPU: {temp}°C ({fanspeed}%)"

    def increase_fanspeed(self):
        speed = round(self.get_fanspeed())
        speed += 5
        self.set_fanspeed(speed)
    
    def reduce_fanspeed(self):
        speed = round(self.get_fanspeed())
        speed -= 5
        self.set_fanspeed(speed)
        
    def get_fanspeed(self):
        f = open('/sys/class/hwmon/hwmon2/pwm2','r')
        speed = int(f.readline().strip())
        f.close()
        return (speed / 255.0) * 100
        
    def set_fanspeed(self, speedvalue):
        if (10 < speedvalue <= 100):
            f = open("/sys/class/hwmon/hwmon2/pwm2","w")
            f.write(str( int((speedvalue * 255) / 100) ) + "\n")
            f.close()

            
    def run(self):
        command = ["sensors"]
        shell = run_through_shell(command)
        answer = shell.out
        pos = answer.find("CPUTIN")
        temp = int(answer[pos + 17 : pos+19])
        color = self.color0
        if(temp >= int(self.threshold1)):
            color = self.color1
        elif(temp >= self.threshold2):
            color = self.color2
        
        formatstring = self.format
        fdict = {
            "temp":  temp,
            "fanspeed": int(round(self.get_fanspeed()))
        }
        self.output = {
            "full_text": formatp(formatstring, **fdict),
            "color": color
        }