import matplotlib.pyplot as plt
a=list()
b=list()
c=list()
d=list()

with open('4.txt','r')as f:
    for line in f.readlines():
        a.append(float(line))

with open('5.txt','r')as f:
    for line in f.readlines():
        b.append(float(line))

with open('6.txt','r')as f:
    for line in f.readlines():
        c.append(float(line))

with open('7.txt','r')as f:
    for line in f.readlines():
        d.append(float(line))
plt.title("Comparing different travel restriction")
plt.plot(a,label='betweeness removal')
plt.plot(b,label='degree difference remvoal')
plt.plot(c,label='degree product removal')
plt.plot(d,label='airport shutdown')
plt.legend()
plt.show()


