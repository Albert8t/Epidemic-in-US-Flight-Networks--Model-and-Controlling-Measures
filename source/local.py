class local():
    def __init__(self,aircode,beta,gamma,sigma1,sigma2,sigsig,nu,nature):
        self.aircode=aircode
        self.nature=nature
        self.S=443900
        self.E=0
        self.I1=0
        self.I2=0
        self.R=0
        self.beta=beta #S to Exposed
        self.gamma=gamma # recover rate
        self.sigma1=sigma1 # expose to infect sympton
        self.sigma2=sigma2 #expose to infect asympton
        self.sigsig=sigsig # from asympton to sympton
        self.nu=nu # vacucation rate

    def nature_propogate(self):
        population=self.S+self.E+self.I1+self.I2+self.R
        deltaS=-self.beta*(self.I1+self.I2)*self.S/population
        deltaE=self.beta*(self.I1+self.I2)*self.S/population-(self.sigma1+self.sigma2)*self.E
        deltaI2=self.sigma2*(self.E)-(self.gamma*self.I2)-self.sigsig*self.I2
        deltaI1=self.sigma1*(self.E)-(self.gamma*self.I1)+self.sigsig*self.I2
        deltaR=self.gamma*(self.I1+self.I2)
        self.S+=deltaS
        self.E+=deltaE
        self.I1+=deltaI1
        self.I2+=deltaI2
        self.R+=deltaR

    def vaccine_propogate(self):
        population=self.S+self.E+self.I1+self.I2+self.R
        deltaS=-self.beta*(self.I1+self.I2)*self.S/population-self.nu*self.S
        deltaE=self.beta*(self.I1+self.I2)*self.S/population-(self.sigma1+self.sigma2)*self.E
        deltaI2=self.sigma2*(self.E)-(self.gamma*self.I2)-self.sigsig*self.I2
        deltaI1=self.sigma1*(self.E)-(self.gamma*self.I1)+self.sigsig*self.I2
        deltaR=self.gamma*(self.I1+self.I2)+self.nu*self.S
        self.S+=deltaS
        self.E+=deltaE
        self.I1+=deltaI1
        self.I2+=deltaI2
        self.R+=deltaR

    def Alert(self):
        alert=False
        population = self.S + self.E + self.I1 + self.I2 + self.R
        if self.E/population> 0.1:
            alert=True
        elif (self.I1+self.I2)/population>0.01:
            alert=True
        return alert


    def population(self):
        return self.S+self.E+self.R+self.I1+self.I2

    def depart(self,S,E,I1,I2,R):
        if self.S>S:
            self.S+=-1*S
        if self.E > E:
            self.E += -1 * E
        if self.I1 > I1:
            self.I1 += -1 * I1
        if self.I2 > I2:
            self.I2 += -1 * I2
        if self.R > R:
            self.R += -1 * R

    def arrive(self,S,E,I1,I2,R):
        self.S+=S
        self.E +=E
        self.I1 +=I1
        self.I2 += I2
        self.R += R






