import core

if __name__=="__main__":
    eventH = core.EventHandler("send")
    eventH.raise_event(core.Events.get_custom("STATUS","cnc initalised",status="init"))
    
    while True:
        i = input("\nmsg:")
        x = core.Events.get_custom("ERROR",i)#{"level":0,"msg":i}
        print(x)
        eventH.raise_event(x)