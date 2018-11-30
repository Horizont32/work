import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.lines as lns

Obj_dist = 1000  # Расстояние до объекта
Full_obj_size = 1200
D_led = 1  # Диаметр светильника
R_ini = D_led / 2  # Минимальный радиус рефлектора
a_ini = 32.5
N = 10**3
num = 16
big_dia = 500
sm_dia = 370
angle_circle_step = float(360 / num)
# zmax = 55.
cree_rad = 32./2

"Calc process"
a = math.radians(a_ini)
z = []
R = []
angle = []
refl_angle = []
refl_angle.append(90.)
angle.append(0.)
z.append(0.)
R.append(R_ini)
z1 = R_ini * math.tan(a)
R1 = R_ini + cree_rad
z.append(z1)
R.append(R1)

# Последнее изменение - добавил cree_rad, чтобы его отменить, надо везде его убрать
# также замут 16 строчки и 75 ( чтобы вернуть - размьютить их), а также замут 76-77

def get_optimized_rad():
    return math.sqrt((Full_obj_size/2)**2 + (big_dia/2)**2 - 2*Full_obj_size/4*big_dia*math.cos(math.radians(angle_circle_step/2)))

# dR = get_optimized_rad() / N
# a_max = pi / 2 - math.atan(get_optimized_rad() / Obj_dist)
# # refl_angle.append(math.degrees(- math.atan(i * (get_optimized_rad() - R[i])/(Obj_dist - z[i]))))
# refl_angle.append(math.degrees(- math.atan((get_optimized_rad() - R[1])/(Obj_dist - z[1]))))
# # refl_angle.append(math.degrees(- math.atan((Obj_dist - z[1])/(get_optimized_rad() - R[1]))))
# while a < a_max and f > 0 and R[i] < 50:
#     print(refl_angle[i], refl_angle[i-1])
#     if abs(refl_angle[i]) < abs(refl_angle[i-1]):
#         a0 = - math.atan(i * (get_optimized_rad() - R[i])/(N * (Obj_dist - z[i])))
#     else:
#         a0 = math.atan(i * get_optimized_rad()/(N * (Obj_dist - z[i])))
#     refl_angle.append(math.degrees(a0))
#     # a0 = 0
#     b = math.pi/2 - a
#     c = math.pi - a0 - b
#     e = (math.pi - c)/2
#     f = b - e
#     if f < 0:
#         break
#     refl = math.pi/2 - f
#     dz = dR * math.tan(refl)
#     i += 1
#     z.append(z[i-1] + dz)
#     R.append(R[i-1] + dR)
#     # z[i] = z[i-1] + dz
#     # R[i] = R[i-1] + dR
#     a = math.atan(z[i]/R[i])
#     angle.append(math.degrees(a))

def rmax():
    thick = 2.
    r_diff_rad = math.sqrt((sm_dia / 2) ** 2 + (big_dia / 2) ** 2 - 0.5 * sm_dia * big_dia * math.cos(
        math.radians(angle_circle_step / 2))) / 2 - 2 * thick - 1
    r_same_rad = sm_dia/2*math.tan(math.radians(angle_circle_step/2)) - thick - 0.5
    return min(r_diff_rad, r_same_rad)

print(rmax())
a0 = math.atan((get_optimized_rad() - cree_rad - R[1])/(Obj_dist - z[1]))
# refl_angle.append(math.degrees(a0))
# Rmax = R[1] + (zmax - z[1]) * math.tan(a0)
Rmax = rmax()
zmax = (rmax() - R[1])/math.tan(a0) + z[1]
print('Максимальный радиус в верхней точке отражателя: ' + str(round(Rmax, 2)) + 'мм.')
a_max = math.atan(zmax/Rmax)
KPD = 100*(get_optimized_rad()-cree_rad)/(Obj_dist/math.tan(a_max))
print('КПД отражателя: ' + str(round(KPD, 2)) + '%')
# da = (a_max - a)/(N-1)
b = math.pi/2. - a
f = (b + a0) / 2.
e = b - f


def calc_p1():
    a0final = math.atan(Rmax/(Obj_dist - zmax))
    bmax = math.pi/2 - a_max
    c_fin = math.pi - a0final - bmax
    e_fin = (math.pi - c_fin)/2
    f_final = bmax - e_fin
    m1 = np.array([[float(math.tan(math.pi/2 - f)), -1.], [float(-math.tan(math.pi/2 - f_final)), 1.]])
    n1 = np.array([float((R[1]/math.tan(f)) - z[1]), zmax - Rmax*math.tan(math.pi/2 - f_final)])
    p1 = np.linalg.solve(m1, n1)
    return p1


def bezier_curve():
    file_list = open('kek.dat', 'w')
    t = 0
    # file_list.write(str((R[1] + 0) / 10 ** 3) + '\t' + str(0. / 10 ** 3) + '\t' + '0.0' + '\n')
    while t <= 1:
        Rc = ((1-t)**2)*R[1] + 2 * (1 - t)*t*calc_p1()[0] + (t**2)*Rmax
        zc = ((1-t)**2)*z[1] + 2 * (1 - t)*t*calc_p1()[-1] + (t**2)*zmax
        t += 1/(N+1)
        file_list.write(str((Rc + 0)/10**3) + '\t' + str(zc/10**3) + '\t' + '0.0' + '\n')
        R.append(Rc)
        z.append(zc)


bezier_curve()


def ang_calc(f, e):
    for i in range(1, len(R)):
        a = math.atan(z[i] / R[i])
        angle.append(math.degrees(a))
        if f >= e:
            if i == 1:
                a0 = math.atan(
                    ((get_optimized_rad() - cree_rad - (i - 1) * (get_optimized_rad()-cree_rad) / (N+1)) - R[i]) / (Obj_dist - z[i]))
            else:
                a0 = math.atan(((get_optimized_rad() - cree_rad - (i-2) * (get_optimized_rad()-cree_rad) / (N+1)) - R[i]) / (Obj_dist - z[i]))
                b = math.pi / 2 - a
                f = (b + a0) / 2
                e = f - a0
        else:
            a0 = math.atan((R[i] - (get_optimized_rad() - cree_rad - (i-2) * (get_optimized_rad()-cree_rad) / (N+1))) / (Obj_dist - z[i]))
            b = math.pi / 2 - a
            c = math.pi - a0 - b
            e = (math.pi - c) / 2
            f = b - e
        refl_angle.append(math.degrees(a0))


ang_calc(f, e)


"""
while a < a_max:
    if f < 0:
        break
    i += 1
    a += da
    angle.append(math.degrees(a))

    # m1 = np.array([[float(math.tan(math.pi/2 - f)), -1.], [float(-math.tan(a)), 1.]])
    # n1 = np.array([float((R[i-1]/math.tan(f)) - z[i-1]), 0.])
    # coord = np.linalg.solve(m1, n1)
    # # print(np.linalg.solve(m1, n1))
    # z.append(coord[-1])
    # R.append(coord[0])
    dz1 = - z[i-1] + R[i-1]*math.tan(a)
    k = dz1*math.tan(f)
    gip = k*math.sin(math.pi/2+f) / math.sin(math.pi/2 - a - f)
    dR = gip*math.cos(a)
    rnew = R[i-1] + dR
    znew = rnew*math.tan(a)
    z.append(znew)
    R.append(rnew)
    print(math.degrees(a), z[i])
    if f >= e:
        a0 = math.atan(((get_optimized_rad() - i * get_optimized_rad()/N) - R[i])/(Obj_dist - z[i]))
        b = math.pi / 2 - a
        f = (b + a0) / 2
        e = f - a0
    else:
        a0 = math.atan((R[i] - (get_optimized_rad() - i * get_optimized_rad()/N))/(Obj_dist - z[i]))
        b = math.pi / 2 - a
        c = math.pi - a0 - b
        e = (math.pi - c) / 2
        f = b - e
    refl_angle.append(math.degrees(a0))
print(R)
print(angle)
print(R[-1])
# print(R)
# print(z)
# refl_angle.append(math.degrees(- math.atan((Obj_dist - z[1])/(get_optimized_rad() - R[1]))))
# while a < a_max and R[i] < 50:
#     a = a + da
#     if f >= e:
#         a0 = math.atan(get_optimized_rad() * kus/(N * (Obj_dist - z[i])))
#         # a0 = math.radians(0)
#         b = math.pi / 2 - a
#         f = (b + a0) / 2
#         e = f - a0
#     else:
#         a0 = math.atan(get_optimized_rad() * kus/(N * (Obj_dist - z[i])))
#         b = math.pi / 2 - a
#         c = math.pi - a0 - b
#         e = (math.pi - c) / 2
#         f = b - e
#     refl_angle.append(math.degrees(a0))
#     # a0 = 0
#     if f < 0:
#         break
#     refl = math.pi/2 - f
#     dz = dR * math.tan(refl)
#     i += 1
#     kus -= 1
#     z.append(z[i-1] + dz)
#     R.append(R[i-1] + dR)
#     # z[i] = z[i-1] + dz
#     # R[i] = R[i-1] + dR
#     a = math.atan(z[i]/R[i])
#     angle.append(math.degrees(a))

"""
def get_object_image():
    r = get_optimized_rad()
    angle_circle = float(0)
    angle_circle_big = angle_circle_step/2
    i = 0
    ax = plt.gcf().gca()
    ax.set_xlim(-1000, 1000)
    ax.set_ylim(-1000, 1000)
    ax.add_artist(plt.Circle((0, 0), Full_obj_size/2, color='r', fill=False))
    for i in range(num):
        x = sm_dia/2 * math.sin(math.radians(angle_circle))
        y = sm_dia/2 * math.cos(math.radians(angle_circle))
        xd = big_dia/2 * math.sin(math.radians(angle_circle_big))
        yd = big_dia/2 * math.cos(math.radians(angle_circle_big))
        angle_circle += angle_circle_step
        angle_circle_big += angle_circle_step
        ax.add_artist(plt.Circle((x, y), r, fill=False))
        ax.add_artist(plt.Circle((xd, yd), r, fill=False))
    plt.savefig('kek.png', dpi=300)
    plt.clf()


def draw_rays():
    ax = plt.gcf().gca()
    ax.set_xlim(-35, 35)
    ax.set_ylim(0, 1000)
    step = 10
    for i in range(1, len(R), step):
        if refl_angle[i] > refl_angle[i-1] and i > 1:
            ax.plot([cree_rad, R[i]], [0, z[i]], color='r', linewidth='0.5')
            ax.plot([R[i], R[i] - (Obj_dist - z[i])*math.tan(math.radians(refl_angle[i]))], [z[i], Obj_dist], color='b', linewidth='0.5')
        else:
            ax.plot([cree_rad, R[i]], [0, z[i]], color='r', linewidth='0.5')
            ax.plot([R[i], R[i] + (Obj_dist - z[i]) * math.tan(math.radians(refl_angle[i]))], [z[i], Obj_dist],
                    color='b', linewidth='0.5')
        ang = math.radians(angle[-1])
        while ang <= math.pi/2:
            ax.plot([0, Obj_dist/math.tan(ang)], [0, Obj_dist], color='y', linewidth='0.5')
            ang += (math.pi/2 - math.radians(angle[-1]))/step
    plt.axis('square')
    plt.savefig('graph.png', dpi=1000)
    plt.show()
    plt.clf()


draw_rays()
get_object_image()
plt.plot(R, z)
# plt.plot(R, angle)
# plt.plot(R, refl_angle)
plt.title('Профиль с КПД %.2f' % KPD + '%')
plt.xlabel('Радиус, мм')
plt.ylabel('Высота, мм')
plt.xlim(R[0] - 5, R[-1] + 5)
plt.grid(True)
plt.axis('square')
plt.savefig('sample.png', dpi=300)