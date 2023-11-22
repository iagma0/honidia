# install/import VPython 3.2

# Set scene
scene = canvas(width=700, height=500)
scene.center = vector(0, 0, 0)
scene.camera.pos += vector(0, 10, 0)
scene.camera.axis += vector(0,-5,0)

# Create a plane of concentric circles
plane0 = cylinder(pos=vector(0, -0.80, 0), axis=vector(0, 0.1, 0), radius=11, color=color.orange)
plane1 = cylinder(pos=vector(0, -0.40, 0), axis=vector(0, 0.1, 0), radius=12, color=color.white)
plane2 = cylinder(pos=vector(0, -0.30, 0), axis=vector(0, 0.1, 0), radius=10, color=color.blue)
plane3 = cylinder(pos=vector(0, -0.20, 0), axis=vector(0, 0.1, 0), radius=6, color=color.green)
plane4 = cylinder(pos=vector(0, -0.10, 0), axis=vector(0, 0.1, 0), radius=2, color=color.red)

# Create a sun
sphere1 = sphere(pos=vector(0, 0, 0), radius=.5, color=color.yellow)
sol_vol = 2*sphere.radius
# Create a moon
lua1 = sphere(pos=vector(0,0,0), radius=0.125, color=color.magenta)
lua2 = sphere(pos=vector(0,0,0), radius=0.2, color=color.cyan)


# Define sphere movement
theta_deg = 0
theta_rad = theta_deg * pi/180
epsilon_rad = 0 # lua1
gamma_rad = 0 # lua2
r = 0 # distance to south pole
r_inc = 0.1 # increment to r
sphere1.rchange = -0.007 # rate of volume change
h_max = 0
h_min = 10
l_max = 0
l_min = 100
# Path tracing
path = curve(color=color.yellow, radius=0.03)
path_lua1 = curve(color=color.magenta, radius=0.01)
path_lua2 = curve(color=color.cyan, radius=0.02)

# Display labels
time_label = label(pos=vec(-12,5,0))
prop_label = label(pos=vec(0,-5,0))

## Set start date
day = 21
hour = 12
month = 6
months = ["Estio", "Pômode", "Nerume", "Ombro", "Nimbo", "Austro", "Geia", "Ôste"]

# Animation loop
while True:
    rate(10)  # animation speed
    theta_deg += 0.0045
    theta_rad = theta_deg * pi/180
    epsilon_rad += 0.25 #0.25
    gamma_rad += 0.1 #0.1
    sol_vol = 2*sphere1.radius
    ## Update label
    hour += 0.11
    if sqrt(r**2) >= 11:
      hour = 0
      day += 1
      if day == 46:
        day = 1
        month += 1
        if month == 8:
          month = 0
    int_hour = int(hour)
    time_label.text = int_hour + "h" + "\n" + months[month] + " " + day
    prop_label.text = "volume = " + str("{:.2f}".format(sol_vol)) + "\n" + "altura = " + str("{:.2f}".format(sphere1.pos.y)) + " (" + str("{:.2f}".format(h_min)) + "/" + str("{:.2f}".format(h_max)) + ")" + "\n" + "luz = " + str("{:.0f}".format((400/sphere1.pos.y)*sol_vol)) + "%" + " (" + str("{:.0f}".format(l_min)) + "/" + str("{:.0f}".format(l_max)) + ")"
   
    ## XZ movement (r, theta)
    r += r_inc
    if sqrt(r**2) >= 11:
      r_inc = -r_inc
    sphere1.pos.x = r*cos(theta_rad)
    sphere1.pos.z = r*sin(theta_rad)
  
    ## Y movement (height)
    sphere1.pos.y = 250/((r+15)**2+25)+3
    path.append(sphere1.pos)
    if h_max < sphere1.pos.y:
      h_max = sphere1.pos.y # record h_max
    if h_min > sphere1.pos.y:
      h_min = sphere1.pos.y # record h_min

    ## Volume oscillation (luminosity)
    sphere1.radius += sphere1.rchange/2
    if sol_vol < 1 and sqrt(r**2) >= 11:
      sphere1.rchange = -sphere1.rchange
    if sqrt(r**2) <= 0.01:
      sphere1.rchange = -sphere1.rchange
    if l_max < (400/sphere1.pos.y)*sol_vol:
      l_max = (400/sphere1.pos.y)*sol_vol # record l_max
    if l_min > (400/sphere1.pos.y)*sol_vol:
      l_min = (400/sphere1.pos.y)*sol_vol # record l_min  
      
    ## Lua1 orbit
    luax = 3*cos(epsilon_rad) + 2*sin(gamma_rad)
    luay = sin(epsilon_rad)**2
    luaz = 3*sin(epsilon_rad)  + 2*cos(gamma_rad)
    lua1.pos = sphere1.pos + vector(luax,luay,luaz)
    path_lua1.append(lua1.pos)
    
     ## Lua2 orbit
    luax2 = 5*cos(gamma_rad)
    luay2 = cos(gamma_rad)**2
    luaz2 = 5*sin(gamma_rad)
    lua2.pos = sphere1.pos + vector(luax2,luay2,luaz2)
    path_lua2.append(lua2.pos)

