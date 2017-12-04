__based on https://github.com/jhoblitt/nginx-rpmbuild/ http://www.thegeekstuff.com/2015/02/rpm-build-package-example/__

**1.Install rpm-build Package**

To build an rpm file based on the spec file that we just created, we need to use rpmbuild command.
rpmbuild command is part of rpm-build package. Install it as shown show below.
    ```
    yum install rpm-build
    ```
rpm-build is dependent on the following package. If you don’t have these installed already, yum will automatically install these dependencies for you.
    ```
    elfutils-libelf
    rpm
    rpm-libs
    rpm-python
    ```
    
**2. RPM Build Directories**
 rpm-build will automatically create the following directory structures that will be used during the RPM build.
```
# ls -lF /root/rpmbuild/
drwxr-xr-x. 2 root root 4096 Feb  4 12:21 BUILD/
drwxr-xr-x. 2 root root 4096 Feb  4 12:21 BUILDROOT/
drwxr-xr-x. 2 root root 4096 Feb  4 12:21 RPMS/
drwxr-xr-x. 2 root root 4096 Feb  4 12:21 SOURCES/
drwxr-xr-x. 2 root root 4096 Feb  4 12:21 SPECS/
drwxr-xr-x. 2 root root 4096 Feb  4 12:21 SRPMS/
```

Note: The above directory structure is for both CentOS and RedHat when using rpmbuild package. You can also use /usr/src/redhat directory, but you need to change the topdir parameter accordingly during the rpm build. If you are doing this on SuSE Enterprise Linux, use /usr/src/packages directory.

If you want to use your own directory structure instead of the /root/rpmbuild, you can use one of the following option:

    Use –buildroot option and specify the custom directory during the rpmbuild
    Specify the topdir parameter in the rpmrc file or rpmmacros file.

**3. Download Source Tar File**

Next, download the source tar file for the package that you want to build and save it under SOURCES directory.

[Nginx 1.13.5](http://nginx.org/download/nginx-1.13.5.tar.gz)
    
[Modsecurity 2.9.2](https://github.com/SpiderLabs/ModSecurity/releases/download/v2.9.2/modsecurity-2.9.2.tar.gz)


**4. Copy nginx configuration files into SOURCES**

Copy whole content of SOURCE folder from this repository to SOURCE folder on your machine

**5. Create nginx.spec file**

Copy nginx.spec file from SPEC folder from this repository to SPEC folder on your machine
   
**6. execute rpmbuild**
    
    
    rpmbuild -ba rpmbuild/SPEC/nginx.spec
    
