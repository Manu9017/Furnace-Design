"""Zinc fume enclosure on the casing deck (ZEN annexure; D-24 wall plane, D-25 door interlock, D-27 west door / kettle cover).

Wall plane = casing outer face. Corner posts stand on the cap beam. Both long sides are open full length below ISMB 300
door-head girts at +2.950:
  * EAST: vertical-lift skimming door with 4 windows, outside the wall plane, on two chain hoists.
  * WEST: insulated skimming door that also becomes the kettle cover. It hangs on two end carriages in guide columns
    outside the wall plane; the hoists lift the carriages 1,000 for skimming; with the carriages seated, worm slew drives
    on the carriages turn the panel 90° inward about its inner bottom edge (+0.450) so it lies on the kettle, hot skin down.
Two roof covers split on the centreline with the 200 mm rope slot and slide outward on end-wall rails. Slot plenums along
both top edges collect into a header outside the north end wall; the Ø700 outlet leaves north then east.
"""
from __future__ import annotations

import math

from ..basis import B, G
from .lib import box, compound, cyl, ibeam, merge, pipe, tube

S2 = (-1, 1)


def _shs(x0, x1, y0, y1, z0, z1, t=6):
    o = box(x0, x1, y0, y1, z0, z1)
    return o.cut(box(min(x0, x1) + t, max(x0, x1) - t, min(y0, y1) + t, max(y0, y1) - t, z0 - 1, z1 + 1))


def _hollow(x0, x1, y0, y1, z0, z1, t=3, open_ends=""):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    ix0 = x0 - 1 if "x" in open_ends else x0 + t
    ix1 = x1 + 1 if "X" in open_ends else x1 - t
    iy0 = y0 - 1 if "y" in open_ends else y0 + t
    iy1 = y1 + 1 if "Y" in open_ends else y1 - t
    return box(x0, x1, y0, y1, z0, z1).cut(box(ix0, ix1, iy0, iy1, z0 + t, z1 - t))


def _rod(p0, p1, r=10):
    return cyl(p0, p1, r)


def _xbrace(p00, p01, p10, p11, r=10):
    """Tie-rod X between two pairs of corners plus turnbuckles at mid-length."""
    rods = [_rod(p00, p11, r), _rod(p01, p10, r)]
    tb = []
    for a, b in ((p00, p11), (p01, p10)):
        m = [(a[i] + b[i]) / 2 for i in range(3)]
        d = [b[i] - a[i] for i in range(3)]
        L = math.sqrt(sum(v * v for v in d))
        u = [v / L for v in d]
        tb.append(cyl([m[i] - 80 * u[i] for i in range(3)], [m[i] + 80 * u[i] for i in range(3)], r + 8))
    return rods + tb


def build_enclosure(R):
    g = G
    xo, yo = g.cXo, g.cYo                               # wall plane = casing outer face
    zb = g.deck
    zt = zb + B.v("enclosure.height")                   # +4.976 top of the top ring
    zg = B.v("enclosure.door_head_z")                   # +2.950 girt underside
    zgt = zg + 300
    slot = B.v("enclosure.rope_slot")
    travel = B.v("enclosure.cover_travel")
    sill = B.v("enclosure.window_sill")
    XI, ZP = B.v("enclosure.west_pivot")               # west door inner face / pivot
    XO = XI - 110
    YD = 3925                                           # west door half-length
    HW = 2450                                           # west door height
    # ================================================================== frame
    cp_ = [_shs(sx * (xo - 150), sx * xo, sy * (yo - 150), sy * yo, zb + 20, zt - 150, 8) for sx in S2 for sy in S2]
    bp = []
    for sx in S2:
        for sy in S2:
            bp.append(box(sx * (xo - 300), sx * xo, sy * (yo - 300), sy * yo, zb, zb + 20))
            bp += [cyl((sx * (xo - d1), sy * (yo - d2), zb + 20), (sx * (xo - d1), sy * (yo - d2), zb + 52), 15) for d1 in (40, 260) for d2 in (40, 260)]
            bp += [box(sx * (xo - 150), sx * (xo - 290), sy * (yo - 81), sy * (yo - 69), zb + 20, zb + 200),
                   box(sx * (xo - 81), sx * (xo - 69), sy * (yo - 150), sy * (yo - 290), zb + 20, zb + 200)]
    R.add("ZEN-01 Corner posts", compound(*cp_, *bp), "enclosure", "zenframe", tag="ZEN-01", title="Corner posts SHS 150 × 150 × 8 with base plates",
          spec="4 posts on 300 × 300 × 20 base plates over the cap-beam corners, 4 × M20 8.8 each into the cap-beam top flange (diaphragms 10 mm inside the box); "
               "2 gussets 12 × 130 × 180 per base; posts +0.276 → +4.826", material="IS 4923 YSt 310 SHS; plates IS 2062 E250; bolts 8.8 HDG",
          src="ZEN annexure · D-24", status="A", note="Member sizes pending the structural check (O-17).", qty="4")
    ip = [_shs(sx * (xo - 120), sx * xo, y - 60, y + 60, zgt, zt - 150) for sx in S2 for y in (-1978, 0, 1978)]
    ep = [_shs(x - 50, x + 50, sy * (yo - 100), sy * yo, zb + 20, zt - 150) for x in (-650, 650) for sy in S2]
    ep += [box(x - 100, x + 100, sy * (yo - 200), sy * yo, zb, zb + 20) for x in (-650, 650) for sy in S2]
    R.add("ZEN-01a Intermediate posts", compound(*ip, *ep), "enclosure", "zenframe", tag="ZEN-01a", title="Intermediate posts",
          spec="Long walls: 3 × SHS 120 × 120 × 6 per side standing on the door-head girt (+3.250 → +4.826) at Y −1.978 / 0 / +1.978; "
               "end walls: 2 × SHS 100 × 100 × 6 per end at X ±650, full height on 200 × 200 × 20 base plates", material="IS 4923 YSt 310",
          src="D-24 · D-27", status="A", qty="10")
    girts = [ibeam((sx * (xo - 70), -(yo - 150), zg + 150), (sx * (xo - 70), yo - 150, zg + 150), h=300, b=140, tw=7.5, tf=12.4) for sx in S2]
    girt_end = [box(sx * (xo - 150), sx * (xo - 10), sy * (yo - 160), sy * (yo - 150), zg, zgt) for sx in S2 for sy in S2]
    R.add("ZEN-02 Door-head girts ISMB 300", compound(*girts, *girt_end), "enclosure", "zenframe", tag="ZEN-02", title="Door-head girts ISMB 300",
          spec=f"Both long sides, underside +{zg / 1000:.3f}, spanning the corner posts (7.91 m) with 12 mm end plates and 4 × M20 each end; "
               "carry the upper wall, the intermediate posts and the slot plenum; the openings below are clear full length",
          material="IS 2062 E250 ISMB 300", src="D-24 · D-27", status="A", note="Deflection under the wall and plenum ≈L/900 (estimate); confirm in O-17.")

    def chan_y(sx):
        return merge(box(sx * (xo - 5.4), sx * xo, -yo, yo, zt - 150, zt), box(sx * (xo - 75), sx * xo, -yo, yo, zt - 9, zt),
                     box(sx * (xo - 75), sx * xo, -yo, yo, zt - 150, zt - 141))

    def chan_x(sy):
        return merge(box(-xo, xo, sy * (yo - 5.4), sy * yo, zt - 150, zt), box(-xo, xo, sy * (yo - 75), sy * yo, zt - 9, zt),
                     box(-xo, xo, sy * (yo - 75), sy * yo, zt - 150, zt - 141))
    lugs = [box(sx * (xo - 60), sx * (xo - 40), sy * (yo - 300), sy * (yo - 180), zt, zt + 90).cut(
        cyl((sx * (xo - 70), sy * (yo - 240), zt + 50), (sx * (xo - 30), sy * (yo - 240), zt + 50), 18)) for sx in S2 for sy in S2]
    R.add("ZEN-03 Top ring ISMC 150", compound(*[chan_y(sx) for sx in S2], *[chan_x(sy) for sy in S2], *lugs), "enclosure", "zenframe", tag="ZEN-03",
          title="Top ring beams ISMC 150 + lifting lugs", spec="Ring at +4.826 → +4.976, mitred corners with cap plates; end beams carry the roof-cover rails; "
               "4 lifting lugs 20 mm with Ø36 holes for erection", material="IS 2062 E250", src="ZEN annexure", status="A")
    # tie-rod bracing: upper long walls (4 bays each side) and end walls (outer bays)
    br = []
    bays = [(-(yo - 150), -2038), (-1918, -60), (60, 1918), (2038, yo - 150)]
    for sx in S2:
        xr = sx * (xo - 76)
        for ya, yb in bays:
            br += _xbrace((xr, ya + 30, zgt + 60), (xr, ya + 30, zt - 210), (xr, yb - 30, zgt + 60), (xr, yb - 30, zt - 210))
    for sy in S2:
        yr = sy * (yo - 50)
        for xa, xb in ((-(xo - 150), -700), (700, xo - 150)):
            br += _xbrace((xa + 30, yr, zb + 300), (xa + 30, yr, 3950), (xb - 30, yr, zb + 300), (xb - 30, yr, 3950))
    R.add("ZEN-01b Tie-rod bracing", compound(*br), "enclosure", "steel", tag="ZEN-01b", title="Tie-rod X-bracing with turnbuckles",
          spec="Ø20 round bar, threaded M20 ends with forged turnbuckles and gusset tabs; upper long walls in 4 bays per side, end walls in the outer bays; "
               "pretension hand-tight + ½ turn; the slot plenums, bolted to the top ring every 1 m, act as horizontal girders against wind", material="IS 2062 E250 round",
          src="this design", status="A", layer="detail")
    # ================================================================== sheeting and stiffeners
    upper = [box(sx * xo, sx * (xo + 3), -yo, yo, zg, zt) for sx in S2]
    ends = []
    for sy in S2:
        e = box(-(xo + 3), xo + 3, sy * yo, sy * (yo + 3), zb, zt)
        if sy > 0:
            for sx in S2:
                e = e.cut(box(sx * 731, sx * 1231, yo - 10, yo + 20, 4126, 4826))
        ends.append(e)
    st = []
    for z in (3550, 4250):          # east: outside; west: inside (the west door rides outside)
        st += [box(xo + 3, xo + 53, -3950, 3950, z, z + 6), box(xo + 47, xo + 53, -3950, 3950, z - 50, z)]
        for ya, yb in ((-3950, -2038), (-1918, -60), (60, 1918), (2038, 3950)):
            st += [box(-xo, -(xo - 50), ya, yb, z, z + 6), box(-(xo - 50), -(xo - 44), ya, yb, z - 50, z)]
    for sy in S2:
        for z in (1100, 1900, 2700, 3500):
            st += [box(-(xo - 150), xo - 150, sy * (yo + 3), sy * (yo + 53), z, z + 6), box(-(xo - 150), xo - 150, sy * (yo + 47), sy * (yo + 53), z - 50, z)]
    R.add("ZEN-04 Wall sheeting", compound(*upper, *ends), "enclosure", "zen", tag="ZEN-04", title="Wall sheeting 3 mm",
          spec="End walls full height; long sides above the door head; sheet flush with the casing outer face, stitch-welded 50 @ 150 to the frame, "
               "seams lapped 50 and sealed with high-temperature silicone; north wall cut for the two slot plenums",
          material="IS 2062 E250 3 mm; inside face zinc-rich epoxy + HR aluminium; outside epoxy + PU RAL 5015", src="ZEN annexure · D-24", status="C")
    R.add("ZEN-04a Sheet stiffeners", compound(*st), "enclosure", "zenframe", tag="ZEN-04a", title="Sheet stiffeners L 50 × 50 × 6",
          spec="Horizontal at ≈700 pitch; east upper wall outside, west upper wall inside (the west door slides outside it)", material="IS 2062 E250", src="ZEN annexure", status="A")
    # ================================================================== EAST door: vertical lift, windows, chain hoists
    gds = []
    for sy in S2:
        gd = box(xo + 3, 1520, sy * 3995, sy * yo, 150, zt - 150)
        gds.append(gd.cut(box(1452, 1518, sy * 3980, sy * 4050, 140, zt)))
    zd0, zd1 = 200, zg - 50
    wins = [(yc, sill, sill + 600) for yc in (-3000, -1000, 1000, 3000)]
    a0, a1 = 1460, 1510
    skin = merge(box(a0, 1463, -4040, 4040, zd0, zd1), box(1507, a1, -4040, 4040, zd0, zd1))
    edge = _hollow(a0, a1, -4040, 4040, zd0, zd1, t=50, open_ends="xX")
    ribs = [box(1463, 1507, y - 20, y + 20, zd0, zd1) for y in (-2000, 0, 2000)]
    rails = [box(1463, 1507, -4040, 4040, z - 20, z + 20) for z in (sill - 60, sill + 660, 2200)]
    door = merge(skin, edge)
    for (yc, z0, z1) in wins:
        door = door.cut(box(a0 - 1, a1 + 1, yc - 300, yc + 300, z0, z1))
    frames = [box(1510, 1525, yc - 350, yc + 350, z0 - 50, z1 + 50).cut(box(1505, 1530, yc - 300, yc + 300, z0, z1)) for (yc, z0, z1) in wins]
    dlugs = [box(1470, 1500, y - 40, y + 40, zd1, zd1 + 80).cut(cyl((1460, y, zd1 + 45), (1510, y, zd1 + 45), 15)) for y in (-3000, 3000)]
    seals = [box(1458, 1462, -4040, 4040, zd0, zd0 + 30)]
    R.add("ZEN-06 East door guides", compound(*gds), "enclosure", "zenframe", tag="ZEN-06", title="East door guide channels",
          spec="Fabricated C-guides 136 × 111 on the corner posts, outside the wall plane, +0.150 → +4.826; UHMW wear strips", material="IS 2062 E250; UHMW-PE",
          src="D-24", status="D")
    R.add("ZEN-07b Skimming door east", compound(door, *ribs, *rails, *frames, *dlugs, *seals), "enclosure", "zen", tag="ZEN-07b",
          title="East skimming door (vertical lift, 4 windows)",
          spec=f"8,080 × {zd1 - zd0:.0f} × 50 framed panel, 3 mm skins on RHS 50 × 50 × 3; 4 × 600 × 600 toughened-glass windows in removable frames, sill +{sill / 1000:.3f}; "
               f"lift {B.v('enclosure.skim_stop'):.0f} to the skimming stop, {B.v('enclosure.door_lift'):.0f} full; silicone rope seals on the edges",
          material="IS 2062 E250; glass 8 mm toughened", src="ZEN annexure · D-24 · D-25", status="D", anim="doorE")
    R.add("ZEN-07bG Door windows east", compound(*[box(1482, 1490, yc - 300, yc + 300, z0, z1) for (yc, z0, z1) in wins]), "enclosure", "glass", tag="ZEN-07bG",
          title="East door windows (4 × 600 × 600 toughened glass)", spec="8 mm toughened glass in removable frames", src="ZEN annexure", status="C", alpha=0.35, anim="doorE")
    zh = zt - 176
    hb = []
    for y in (-3000, 3000):
        hb += [box(xo + 3, 1600, y - 60, y + 60, zt - 40, zt), box(1400, 1570, y - 120, y + 120, zh, zt - 40), cyl((1485, y, zh - 60), (1485, y, zh), 30)]
    prox = [box(1520, 1550, 4020, 4060, z, z + 40) for z in (zd0 + 20, zd0 + 20 + B.v("enclosure.skim_stop"), zd0 + 20 + B.v("enclosure.door_lift"))]
    R.add("ZEN-08b Door hoists east", compound(*hb, *prox), "enclosure", "motor", tag="ZEN-08b", title="East door chain hoists (2 × 1 t, synchronised)",
          spec="2 electric chain hoists 1 t at 8 m/min on brackets off the top ring; inductive proximity limits: closed / skimming stop / full lift; slack-chain switch",
          src="ZEN annexure", status="C")
    top_ch = zh - 60
    R.add("ZEN-08bC Hoist chains east", compound(*[cyl((1485, y, zd1 + 45), (1485, y, top_ch), 8) for y in (-3000, 3000)]), "enclosure", "chain", tag="ZEN-08bC",
          title="East hoist load chains", spec="Shown at the closed position", src="ZEN annexure", status="C", anim=f"chainE:{top_ch:.0f}")
    # ================================================================== WEST door: skimming door + kettle cover (D-27)
    zw0, zw1 = ZP, ZP + HW
    inner = box(XI - 3, XI, -YD, YD, zw0, zw1)                  # 3 mm SS 304 hot skin (faces the kettle, becomes the underside)
    outer = box(XO, XO + 2, -YD, YD, zw0, zw1)
    core = box(XO + 2, XI - 3, -YD + 50, YD - 50, zw0 + 50, zw1 - 50)
    frm = _hollow(XO + 2, XI - 3, -YD, YD, zw0, zw1, t=50, open_ends="xX")
    vert = [box(XO + 2, XI - 3, y - 25, y + 25, zw0, zw1) for y in (-1960, 0, 1960)]
    hor = [box(XO + 2, XI - 3, -YD, YD, z - 25, z + 25) for z in (zw0 + 1225,)]
    pw = [(yc, sill, sill + 300) for yc in (-3000, -1000, 1000, 3000)]
    panel = merge(inner, outer, frm, *vert, *hor)
    corew = core
    for m in (*vert, *hor):
        corew = corew.cut(m.translate((0, 0, 0)))
    for (yc, z0, z1) in pw:
        panel = panel.cut(box(XO - 1, XI + 1, yc - 150, yc + 150, z0, z1))
        corew = corew.cut(box(XO - 1, XI + 1, yc - 170, yc + 170, z0 - 20, z1 + 20))
    pins = [cyl((XI, sy * (YD - 50), ZP), (XI, sy * 3990, ZP), 40) for sy in S2]
    endseal = [box(XO, XI, sy * YD, sy * (YD + 10), zw0, zw1) for sy in S2]
    topseal = box(XO, XI, -YD, YD, zw1, zw1 + 15)
    anim_w = f"rotW:{XI:.0f}:{ZP:.0f}"
    R.add("ZEN-07a West door / kettle cover", compound(panel, *pins, *endseal, topseal), "enclosure", "ss", tag="ZEN-07a",
          title="West skimming door that becomes the kettle cover",
          spec=f"7,850 × 2,450 × 110 insulated panel: 3 mm SS 304 hot skin (faces the bath; underside when lowered), 75 mm blanket 128 kg/m³ + 25 mm microporous, 2 mm MS outer skin, "
               f"RHS 100 × 50 × 4 frame with 3 posts and a mid rail; Ø80 pivot pins on the inner bottom edge at +{ZP / 1000:.3f}; "
               f"positions: CLOSED (vertical), SKIMMING (lifted {B.v('enclosure.skim_stop'):.0f} on the carriages), KETTLE COVER (turned 90° inward; lies at +0.450 → +0.560 "
               "over X −1.554 → +0.896, i.e. the whole kettle and flange); silicone-glass rope seals on the ends and head; ≈1.4 t",
          material="SS 304 + IS 2062 E250; blanket 1260 grade 128 kg/m³", src="Owner instruction 21 Nov · D-27", status="D",
          note="Interlocks: turns only with both carriages seated and no jig over the bath; lifts only when vertical.", anim=anim_w)
    R.add("ZEN-07aI West door insulation core", corew, "enclosure", "insul", tag="ZEN-07aI", title="West door insulation core (75 blanket + 25 microporous)",
          spec="75 mm ceramic-fibre blanket 128 kg/m³ 1260 grade on the hot side + 25 mm microporous panel on the cold side, staggered joints; SS 304 pins @ 300 with speed washers "
               "on the hot skin; top skin ≈77 °C when it lies on the bath (C-15)", src="D-27 · C-15", status="D", anim=anim_w)
    R.add("ZEN-07aG West door sight windows", compound(*[box(XI - 60, XI - 50, yc - 150, yc + 150, z0, z1) for (yc, z0, z1) in pw]), "enclosure", "glass",
          tag="ZEN-07aG", title="West door sight windows (4 × 300 × 300 glass-ceramic)", spec="5 mm glass-ceramic (700 °C) in SS frames; smaller than the east windows because this panel is also the cover (A-13)",
          src="ZEN annexure · D-27", status="D", alpha=0.35, anim=anim_w)
    # guide columns on the furnace-pit wall top, carriages with slew drives, hoists
    gcol = []
    for sy in S2:
        y0, y1 = sy * 4030, sy * 4080
        gcol += [box(-1700, -1520, y0, y1, 20, 4780).cut(box(-1690, -1530, sy * 4020, sy * 4070, 0, 4790)),
                 box(-1720, -1500, sy * 3990, sy * 4075, 0, 20), box(-1720, -1500, sy * 3930, sy * 4090, 4780, 4820),
                 box(-1520, -1384, sy * 4040, sy * 4060, 4400, 4500)]
    R.add("ZEN-05w West door guide columns", compound(*gcol), "enclosure", "zenframe", tag="ZEN-05w", title="West door guide columns and hoist beams",
          spec="Fabricated C-columns 180 × 50 on 220 × 110 × 20 base plates on the furnace-pit wall top (2 × M20 chemical anchors), tied to the corner posts at +4.45; "
               "hoist beams on top at +4.80", material="IS 2062 E250", src="D-27", status="D")
    car = []
    for sy in S2:
        car += [box(-1700, -1420, sy * 4010, sy * 4030, ZP - 200, ZP + 400),
                cyl((XI, sy * 3935, ZP), (XI, sy * 4010, ZP), 150),
                cyl((XI - 150, sy * 3972, ZP + 100), (XI - 380, sy * 3972, ZP + 100), 60),
                box(-1640, -1580, sy * 4010, sy * 4030, ZP + 400, ZP + 420)]
        car += [cyl((x, sy * 4030, z), (x, sy * 4068, z), 22) for x in (-1665, -1555) for z in (ZP - 150, ZP + 350)]
    R.add("ZEN-05c West door carriages and slew drives", compound(*car), "enclosure", "motor", tag="ZEN-05c", title="West door end carriages with worm slew drives",
          spec="Carriage 20 mm side plate with 4 Ø44 guide rollers; worm slew drive on the pivot axis, self-locking, ≥ 10 kN·m output / 30 kN·m holding, "
               "0.75 kW brake motor + encoder, synchronised by VFD (C-15: 8.4 kN·m per end needed at horizontal)", src="D-27", status="A", anim="doorW")
    hz = 4650
    wh = []
    for sy in S2:
        wh += [box(-1660, -1560, sy * 3940, sy * 4020, hz, 4780), cyl((-1610, sy * 3980, hz - 60), (-1610, sy * 3980, hz), 30)]
        wh += [box(-1720, -1700, sy * 4040, sy * 4070, z, z + 40) for z in (ZP + 450, ZP + 1450, ZP + 120)]
    R.add("ZEN-08a West door hoists", compound(*wh), "enclosure", "motor", tag="ZEN-08a", title="West door carriage hoists (2 × 2 t) and limits",
          spec="2 electric chain hoists 2 t at 4 m/min on the guide-column tops, synchronised; proximity limits: carriages seated / skimming stop; "
               "slew-drive encoder limits: vertical / cover (90°); latch-out of the turn unless both carriages are seated", src="D-27", status="D")
    ch_top = hz - 60
    R.add("ZEN-08aC Hoist chains west", compound(*[cyl((-1610, sy * 3980, ZP + 420), (-1610, sy * 3980, ch_top), 8) for sy in S2]), "enclosure", "chain",
          tag="ZEN-08aC", title="West hoist load chains", spec="Shown with the carriages seated", src="D-27", status="D", anim=f"chainW:{ch_top:.0f}")
    hs = [box(XI + 2, -xo, -YD, YD, zg - 45, zg - 35), box(XI + 45, -xo, -3800, 3800, 430, 445),
          box(-xo - 23, -xo - 3, -3956, -YD - 10, ZP, zg), box(-xo - 23, -xo - 3, YD + 10, 3956, ZP, zg)]
    rests = [merge(box(810, 890, y - 40, y + 40, zb, ZP - 5), box(800, 900, y - 50, y + 50, ZP - 5, ZP)) for y in (-3000, -1000, 1000, 3000)]
    R.add("ZEN-07aS West door head, sill and jamb seals", compound(*hs), "enclosure", "rubber", tag="ZEN-07aS", title="West opening head brush, sill plate and jamb brushes",
          spec="Head: horizontal brush strip on the girt edge reaching the door's inner face (the door passes under it when it turns); sill: 6 mm plate on the cap-beam edge at +0.430; "
               "jambs: vertical brush strips on the corner posts", src="D-27", status="D")
    R.add("ZEN-07aR Kettle-cover rest posts", compound(*rests), "enclosure", "steel2", tag="ZEN-07aR", title="Kettle-cover rest posts on the east deck",
          spec="4 × SHS 80 × 80 × 5 posts over the support ribs at Y ±1.0 / ±3.0 m, 100 × 100 caps with 5 mm fibre-paper pads, top +0.450; take the cover's far edge",
          material="IS 4923; fibre paper 1260", src="D-27", status="D", qty="4")
    # ================================================================== roof covers
    yr0, yr1 = yo - 75, yo - 40
    rails, outr = [], []
    for sy in S2:
        rails += [box(-3000, 3000, sy * yr0, sy * yr1, zt, zt + 30), box(-3000, 3000, sy * (yo - 32), sy * (yo - 2), zt, zt + 40)]
        rails += [box(sx * 2950, sx * 3000, sy * (yo - 80), sy * (yo - 35), zt + 30, zt + 110) for sx in S2]
        for sx in S2:
            outr += [merge(box(sx * (xo + 3), sx * 3000, sy * (yo - 5.4), sy * yo, zt - 150, zt), box(sx * (xo + 3), sx * 3000, sy * (yo - 75), sy * yo, zt - 9, zt),
                           box(sx * (xo + 3), sx * 3000, sy * (yo - 75), sy * yo, zt - 150, zt - 141))]
        outr.append(cyl((1561, sy * (yo - 40), zt - 1000), (2500, sy * (yo - 40), zt - 151), 40))
        outr.append(cyl((-1745, sy * 4055, zt - 900), (-2500, sy * 4055, zt - 151), 40))
    lim = [box(sx * x - 30, sx * x + 30, yo + 5, yo + 45, zt - 60, zt) for sx in S2 for x in (1330, 2950)]
    drag = [box(sx * 1500, sx * 2950, yo + 60, yo + 160, zt - 140, zt - 60) for sx in S2]
    R.add("ZEN-05 Cover rails and outriggers", compound(*rails, *outr), "enclosure", "zenframe", tag="ZEN-05", title="Roof-cover rails, racks, buffers and outriggers",
          spec=f"Rail 35 × 30 EN8 and m4 rack on both end beams, extended on ISMC 150 outriggers with Ø80 knee braces to X ±3.0 m; rubber end buffers; travel {travel:.0f} per cover",
          material="Rail EN8; rack C45 induction hardened", src="ZEN annexure · D-24", status="D")
    R.add("ZEN-05a Cover limit switches", compound(*lim, *drag), "enclosure", "yellow", tag="ZEN-05a", title="Roof-cover limit switches and cable drag chains",
          spec="2 limit switches per cover (closed / open) on the north rail; nylon drag chains carry the drive cables", src="ZEN annexure", status="C")
    zc0 = zt + 150
    for sx, nm in ((-1, "west"), (1, "east")):
        xa, xb = sx * slot / 2, sx * (xo + 100)
        fr = box(xa, xb, -(yo + 100), yo + 100, zc0, zc0 + 100).cut(box(sx * (slot / 2 + 50), sx * (xo + 50), -(yo + 50), yo + 50, zc0 - 1, zc0 + 101))
        cross = [box(xa, xb, y - 25, y + 25, zc0, zc0 + 100) for y in (-2700, -1350, 0, 1350, 2700)]
        sheet = box(xa, xb, -(yo + 100), yo + 100, zc0 + 100, zc0 + 103)
        ins = box(sx * (slot / 2 + 30), sx * (xo + 70), -3970, 3970, zc0 - 51, zc0)
        seal = box(sx * slot / 2, sx * (slot / 2 + 25), -(yo + 100), yo + 100, zt + 60, zc0)
        carr, wh2 = [], []
        for sy in S2:
            carr.append(box(sx * 250, sx * 1350, sy * (yo - 120), sy * (yo + 10), zt + 100, zc0))
            carr += [box(sx * x - 20, sx * x + 20, sy * (yo - 90), sy * (yo - 80), zt - 20, zt + 100) for x in (400, 1200)]
            wh2 += [cyl((sx * x, sy * (yo - 77.5), zt + 80), (sx * x, sy * (yo - 37.5), zt + 80), 50) for x in (400, 1200)]
            wh2.append(cyl((sx * 850, sy * (yo - 32), zt + 82), (sx * 850, sy * (yo - 2), zt + 82), 42))
        shaft = cyl((sx * 850, -(yo - 2), zt + 82), (sx * 850, yo - 2, zt + 82), 25)
        pb = [box(sx * 800, sx * 900, y - 50, y + 50, zt + 60, zt + 100) for y in (-2700, 0, 2700)]
        motor = merge(box(sx * 760, sx * 940, yo + 10, yo + 260, zt + 30, zt + 230), cyl((sx * 850, yo - 2, zt + 82), (sx * 850, yo + 10, zt + 82), 25))
        R.add(f"ZEN-09{'a' if sx < 0 else 'b'} Roof cover {nm}", compound(fr, *cross, sheet, ins, seal, *carr, *wh2, shaft, *pb), "enclosure", "zen",
              tag=f"ZEN-09{'a' if sx < 0 else 'b'}", title=f"Sliding roof cover, {nm}",
              spec=f"{abs(xb - xa):,.0f} × {2 * (yo + 100):,.0f}: ISMC 100 frame, 3 mm top sheet, 50 mm fibre + 1 mm SS 304 liner underneath; end carriages with 2 flanged "
                   f"Ø100 wheels and anti-lift hooks each; line shaft Ø50 with pinions on both racks; brush seal on the {slot:.0f} mm rope slot",
              material="IS 2062 E250; SS 304 liner", src="ZEN annexure · D-24", status="C", anim=f"roof{'W' if sx < 0 else 'E'}")
        R.add(f"ZEN-09{'a' if sx < 0 else 'b'}M Cover drive {nm}", motor, "enclosure", "motor", tag=f"ZEN-09{'a' if sx < 0 else 'b'}M",
              title=f"Roof-cover drive, {nm}: 0.5 HP geared motor, VFD", spec="Helical-bevel 0.37 kW with brake on the north carriage, driving the line shaft; soft start/stop ramps",
              src="ZEN annexure", status="C", anim=f"roof{'W' if sx < 0 else 'E'}")
    # ================================================================== lighting, instruments, electrics
    lamps, lens = [], []
    for sy in S2:
        for x in (-350, 350):
            lamps += [box(x - 150, x + 150, sy * (yo - 200), sy * (yo - 60), zt - 760, zt - 540), box(x - 30, x + 30, sy * (yo - 60), sy * yo, zt - 680, zt - 620)]
            lens.append(box(x - 130, x + 130, sy * (yo - 206), sy * (yo - 200), zt - 740, zt - 560))
    R.add("ZEN-10 LED floods", compound(*lamps), "enclosure", "black", tag="ZEN-10", title="LED floodlights 4 × 200 W",
          spec="Two on each end wall, inside, aimed at the bath; IP66, 80 °C ambient rated, toughened lens, SS brackets", src="ZEN annexure", status="C")
    R.add("ZEN-10a LED flood lenses", compound(*lens), "enclosure", "lamp", tag="ZEN-10a", title="LED flood lenses", spec="IP66", src="ZEN annexure", status="C")
    te = merge(cyl((500, yo - 10, 3800), (500, yo - 160, 3800), 8), box(460, 540, yo + 3, yo + 83, 3760, 3840))
    dp = merge(cyl((-500, yo - 10, 3800), (-500, yo + 3, 3800), 6), box(-580, -420, yo + 3, yo + 93, 3720, 3880))
    lcs = merge(box(1560, 1660, -3600, -3500, 0, 1000), box(1540, 1680, -3700, -3400, 1000, 1500), *[cyl((1540, y, 1350), (1520, y, 1350), 18) for y in (-3640, -3580, -3520, -3460)],
                cyl((1540, -3550, 1150), (1515, -3550, 1150), 28))
    tray = [box(sx * (xo - 140), sx * (xo + 10), -3700, 3700, zt, zt + 60).cut(box(sx * (xo - 130), sx * xo, -3701, 3701, zt + 5, zt + 61)) for sx in S2]
    jb = [box(sx * (xo + 3), sx * (xo + 103), y - 100, y + 100, zt - 500, zt - 300) for sx in S2 for y in (-1000, 1000)]
    R.add("ZEN-14 Enclosure instruments and control station", compound(te, dp, lcs), "instr", "panel", tag="ZEN-14", title="Enclosure TE, draft ΔP and local control station",
          spec="Pt100 at +3.8 inside the north wall; draft ΔP transmitter ±100 Pa (target −5 to −10 Pa); LCS at the SE corner: roof open/close, east door up/stop/down, "
               "west door skim/close/cover, lamp test, emergency stop (mushroom, latching)", src="this design", status="D")
    R.add("ZEN-14a Cable trays and junction boxes", compound(*tray, *jb), "enclosure", "galv", tag="ZEN-14a", title="Cable trays on the top ring and junction boxes",
          spec="Perforated GI tray 150 × 50 on the long top beams; IP65 junction boxes on the upper walls; FRLS armoured cables, 90 °C insulation",
          material="HDG tray", src="this design", status="D")
    # ================================================================== extraction: slot plenums, header, outlet
    zd_a, zd_b = 4126, 4826
    lat, cdoors = [], []
    for sx in S2:
        d = _hollow(sx * 731, sx * 1231, -4050, yo + 3, zd_a, zd_b, open_ends="Y")
        for yc in range(-3500, 3501, 1000):
            d = d.cut(box(sx * 725, sx * 737, yc - 350, yc + 350, zd_a + 60, zd_a + 90))
        lat.append(d)
        cdoors += [box(sx * 880, sx * 1180, y - 200, y + 200, zd_a - 8, zd_a) for y in (-2500, 0, 2500)]
        cdoors += [box(sx * 1231, sx * (xo - 75), y - 30, y + 30, zd_b - 40, zd_b) for y in (-3000, -1000, 1000, 3000)]
    R.add("ZEN-11 Lateral slot plenums", compound(*lat), "enclosure", "galv", tag="ZEN-11", title="Lateral slot plenums 500 × 700",
          spec="Inside both top edges, 3 mm MS; 8 slots 700 × 30 per side on the inner face (≈16.5 m/s) with sliding SS shutters for balancing; "
               "10,000 m³/h per side, plenum 7.9 m/s at the north end (under half the slot velocity, C-15)", material="IS 2062 E250; shutters SS 304",
          src="ZEN annexure · C-15", status="D")
    R.add("ZEN-11a Plenum cleaning doors and brackets", compound(*cdoors), "enclosure", "steel2", tag="ZEN-11a", title="Plenum cleaning doors and girder brackets",
          spec="3 bolted cleaning doors 300 × 400 under each plenum (ZnCl₂/NH₄Cl dust settles in the plenum); brackets @ 2 m tie the plenum to the top ring",
          src="C-15", status="D")
    hdr = _hollow(-1261, 1261, yo + 3, yo + 603, zd_a, zd_b).cut(cyl((0, yo + 590, 4476), (0, yo + 610, 4476), 350))
    for sx in S2:
        hdr = hdr.cut(box(sx * 734, sx * 1228, yo, yo + 8, zd_a + 3, zd_b - 3))
    yo2, zo = 5300, 4476
    out = pipe([(0, yo + 603, zo), (0, yo2, zo), (4600, yo2, zo)], 350).cut(pipe([(0, yo + 590, zo), (0, yo2, zo), (4620, yo2, zo)], 347))
    fl = tube((4600, yo2, zo), (4620, yo2, zo), 420, 347)
    col = merge(box(3925, 4075, yo2 - 75, yo2 + 75, 0, zo - 400), box(3800, 4200, yo2 - 400, yo2 + 400, zo - 400, zo - 350), box(3800, 4200, yo2 - 200, yo2 + 200, 0, 20))
    dmp = merge(tube((2400, yo2, zo), (2500, yo2, zo), 400, 350), box(2420, 2480, yo2 - 60, yo2 + 60, zo + 400, zo + 600), box(2380, 2520, yo2 - 120, yo2 + 120, zo + 600, zo + 760))
    R.add("ZEN-12 Suction header", hdr, "enclosure", "galv", tag="ZEN-12", title="Suction header 600 × 700 outside the north end wall",
          spec="Joins both slot plenums; Ø700 outlet on the north face; 13.2 m/s; drain/cleanout at each end", src="ZEN annexure · D-24", status="D")
    R.add("ZEN-13 Outlet duct Ø700", merge(out, fl), "enclosure", "galv", tag="ZEN-13", title="Outlet duct Ø700 to the zinc-fume bag filter",
          spec="20,000 m³/h, 14.4 m/s; 4 mm MS, long-radius (1.5 D) bends; north then east at +4.476 to a flanged stub at X +4.6 m", src="HDG · ZEN annexure", status="A",
          note="Bag-filter (ZFE) location and fan are open (O-16).")
    R.add("ZEN-13a Outlet duct support", col, "enclosure", "zenframe", tag="ZEN-13a", title="Outlet duct support column", spec="ISHB 150 with saddle and U-strap", src="this design", status="D")
    R.add("ZEN-13b Outlet isolation damper", dmp, "enclosure", "red", tag="ZEN-13b", title="Outlet isolation / turndown damper Ø700",
          spec="Butterfly Ø700, 5 mm disc, SS 304 shaft, electric actuator; closes to 50 % flow in kettle-cover mode (C-15)", src="this design", status="D")
