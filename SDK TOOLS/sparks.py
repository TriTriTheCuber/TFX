import os
import re
from pathlib import Path
import random
flight_model = "flight_model.cfg"
newfile = "f.txt"
points = []
size = input("Please input the size of the water splash (use one as default)")
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
        randid = random.randint(0,100000000000000000000)
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
        lines.append(f"""    <Component ID="FX_WaterSplash_C{p}">""")
        lines.append("""        <OverrideTemplateParameters>""")
        lines.append(f"""            <FX_CODE>(L:WaterTimer:{p}, number) 0 > if{{ 1 }} els{{ 0 }}</FX_CODE>""")
        lines.append(f"""            <FX_GRAPH_PARAM_0>Contact#, {p}</FX_GRAPH_PARAM_0>""")
        lines.append(f"""            <FX_GRAPH_PARAM_1>Size, {size}</FX_GRAPH_PARAM_1>""")
        lines.append(f"""            <FX_GRAPH_PARAM_2>randid, {randid}</FX_GRAPH_PARAM_2>""")
        lines.append("""            <FX_GUID>{D0BC5EEA-8816-4D78-B33E-9EF6E23BD52C}</FX_GUID>""")
        lines.append(f"""            <FX_NAME>FX_SPLASH_{p}</FX_NAME>""")
        lines.append("""        </OverrideTemplateParameters>""")
        lines.append(f"""        <Component ID="FX_SPLASH{p}" Node="__NO_NODE__">""")
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
        lines.append(f"""                   0 (>L:WaterTimer:{p}, number)""")
        lines.append("""                }""")
        lines.append("""                els{""")
        lines.append(f"""                   (L:ScrapeTimer:{p}, number) 0 > if{{""")
        lines.append(f"""                       (L:ScrapeTimer:{p}, number) (E:SIMULATION DELTA TIME, number) - 0 max (>L:ScrapeTimer:{p}, number)""")
        lines.append("""                    }""")
        lines.append("""                }""")
        lines.append("")
        lines.append(f"""               (A:CONTACT POINT WATER DEPTH:{p}, ft) 0 > if{{""")
        lines.append(f"""                   0.5 (>L:WaterTimer:{p}, number)""")
        lines.append(f"""                   0 (>L:ScrapeTimer:{p}, number)""")
        lines.append("""                }""")
        lines.append("""                els{""")
        lines.append(f"""                   (L:WaterTimer:{p}, number) 0 > if{{""")
        lines.append(f"""                       (L:WaterTimer:{p}, number) (E:SIMULATION DELTA TIME, number) - 0 max (>L:WaterTimer:{p}, number)""")
        lines.append("""                    }""")
        lines.append("""                }""")

    lines.append("")
    lines.append("""            </UPDATE_CODE>""")
    lines.append("""        </UseTemplate>""")
    lines.append("""    </Component>""")


    lines = "\n".join(lines)
    n.write(lines)