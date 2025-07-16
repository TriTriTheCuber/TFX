# Place this file in Plane/simobjects/airplanes/plane and run it, it will do all the spark stuff for you!
# Output of the script is f.txt
import os
import re
from pathlib import Path
flight_model = "flight_model.cfg"
newfile = "f.txt"
points = []
with open(flight_model, "r") as fm:
    f = fm.readlines()
    for l in f:
        if l.startswith("point."):
            match = re.search(r"point.(.+?)\s*=", l)
            if match:
                num = match.group(1)
            match = re.search(r"=\s*2", l)
            if match:
                points.append(num)
print(points)
if os.path.isfile(newfile):
    os.remove(newfile)
with open(newfile,"x") as n:
    lines = []
    for p in points:
        lines.append(f"""    <Component ID="FX_SPARKS_C{p}">""")
        lines.append("""        <OverrideTemplateParameters>""")
        lines.append(f"""            <FX_CODE>(L:ScrapeTimer:{p}, number) 0 > if{{ 1 }} els{{ 0 }}</FX_CODE>""")
        lines.append("""            <FX_GUID>{0208217C-8EBE-4673-AB47-2E7E0B969083}</FX_GUID>""")
        lines.append(f"""            <FX_NAME>FX_SPARKS_{p}</FX_NAME>""")
        lines.append("""        </OverrideTemplateParameters>""")
        lines.append(f"""        <Component ID="FX_SPARK{p}" Node="__NO_NODE__">""")
        lines.append("""            <UseTemplate Name="ASOBO_GT_FX">""")
        lines.append(f"""                <FX_CONTACT_POINT_ID>{p}</FX_CONTACT_POINT_ID>""")
        lines.append("""            </UseTemplate>""")
        lines.append("""        </Component>""")
        lines.append("""    </Component>""")
        lines.append("")
    lines.append("")
    lines.append("")

    lines.append("""    <Component ID="ScrapeEffectTimer">""")
    lines.append("""        <UseTemplate Name="ASOBO_GT_Update">""")
    lines.append("""            <ANIM_CODE>1</ANIM_CODE>""")
    lines.append("""            <FREQUENCY>60</FREQUENCY>""")
    lines.append("""            <UPDATE_CODE>""")
    for p in points:
        lines.append("")
        lines.append(f"""               (A:CONTACT POINT IS ON GROUND:{p}, bool) 1 == if{{""")
        lines.append(f"""                   0.5 (>L:ScrapeTimer:{p}, number)""")
        lines.append("""                }""")
        lines.append("""                els{""")
        lines.append(f"""                   (L:ScrapeTimer:{p}, number) 0 > if{{""")
        lines.append(f"""                       (L:ScrapeTimer:{p}, number) (E:SIMULATION DELTA TIME, number) - 0 max (>L:ScrapeTimer:{p}, number)""")
        lines.append("""                    }""")
        lines.append("""                }""")
    lines.append("")
    lines.append("""            </UPDATE_CODE>""")
    lines.append("""        </UseTemplate>""")
    lines.append("""    </Component>""")


    lines = "\n".join(lines)
    n.write(lines)
