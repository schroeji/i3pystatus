from i3pystatus.core.command import run_through_shell
from i3pystatus import IntervalModule, formatp


class nvidiatemp(IntervalModule):

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
    
    format = "GPU: {temp}°C"
    
            
    def run(self):
        
        command = ["nvidia-settings", "-query", "GPUCoreTemp", "-t"]
        shell = run_through_shell(command)
        answer = shell.out
        temp = int(answer[-3 : -1])
        color = self.color0
        
        if(temp >= int(self.threshold1)):
            color = self.color1
        elif(temp >= self.threshold2):
            color = self.color2
        
        formatstring = self.format
        fdict = {
            "temp":  temp,
        }
        self.output = {
            "full_text": formatp(formatstring, **fdict),
            "color": color
        }