from sklearn.cross_decomposition import PLSRegression
from sklearn import kernel_approximation as ks
from sklearn import preprocessing


class KPLS(PLSRegression):
    def __init__(self, x, y, copy=True, max_iter=500, n_components=1, nkernel_components=100, scale=True, tol=1e-6,
                 kernel='linear', preprocess=True, gamma=None, coef0=1, degree=3):
        super(KPLS, self).__init__(copy=copy, max_iter=max_iter, n_components=n_components, scale=scale, tol=tol)

        self.x = x
        self.y = y
        self.kernel = kernel
        self.preprocess = preprocess
        self.gamma = gamma
        self.coef0 = coef0
        self.degree = degree
        self.nkernel_components = nkernel_components

        self.kX = ks.Nystroem(kernel=self.kernel, gamma=self.gamma, coef0=self.coef0, degree=self.degree,
                              n_components=self.nkernel_components)
        self.Xkernel = self.kX.fit_transform(x)

        if self.preprocess:
            self.Xscaler = preprocessing.StandardScaler().fit(self.Xkernel)
            self.Xkernel = self.Xscaler.transform(self.Xkernel)

    def construct_kpls_model(self):
        self.kpls = PLSRegression(self.n_components)
        self.kpls.fit(self.Xkernel, self.y)

    def convert_to_kernel(self, x_test):
        Xkernel = self.kX.transform(x_test)
        if self.preprocess:
            xkernel = self.Xscaler.transform(Xkernel)

        return xkernel

    def kpls_predict(self, x_test):
        xkernel = self.convert_to_kernel(x_test)
        return self.kpls.predict(xkernel)
