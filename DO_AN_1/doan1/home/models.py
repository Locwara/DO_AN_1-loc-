
from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
# Create your models here.,..
from django.utils import timezone
from django.contrib.auth import get_user_model

        

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('Username là bắt buộc')
        if not email:
            raise ValueError('Email là bắt buộc')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        return self.create_user(username, email, password, **extra_fields)



class CustomUser(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = [
        ('pending', 'Chờ duyệt'),
        ('approved', 'Đã duyệt'),
        ('rejected', 'Từ chối'),
    ]
    
    username = models.CharField(max_length=40, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    tentk = models.CharField(max_length=20)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.username
class Calam(models.Model):
    macalam = models.AutoField(primary_key=True) 
    manv = models.ForeignKey('Nhanvien', on_delete=models.CASCADE, db_column='manv')
    ngay = models.DateField()
    giobd = models.TimeField()
    giokt = models.TimeField()

    class Meta:
        db_table = 'calam'
    
class Nghiphep(models.Model):
    manp = models.AutoField(max_length=10, primary_key=True)
    manv = models.ForeignKey('Nhanvien', on_delete=models.CASCADE, db_column='manv')
    ngaybd = models.DateField()
    ngaykt = models.DateField()
    lydonghi = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'nghiphep'
        
        
class Bangluong(models.Model):
    maluong = models.AutoField(max_length=10, primary_key=True)
    manv = models.ForeignKey('Nhanvien', on_delete=models.CASCADE, db_column='manv')
    thangluong = models.DateField()
    sogio = models.FloatField()
    luongcoban = models.FloatField()
    tongluong = models.FloatField()

    class Meta:
        db_table = 'bangluong'

    def save(self, *args, **kwargs):
        if self.sogio is not None and self.luongcoban is not None:
            self.tongluong = self.sogio * self.luongcoban
        else:
            self.tongluong = 0  

        super().save(*args, **kwargs)

class Nhanvien(models.Model):
    GENDER_CHOICES = [
        (True, 'Nam'),
        (False, 'Nữ'),
    ]
    
    # Định nghĩa choices cho vị trí công việc
    PHUC_VU = 'Nhân viên phục vụ'
    PHA_CHE = 'Nhân viên pha chế' 
    KHO = 'Nhân viên kho'
    QUAN_LY = 'Quản lý'
    
    CV_CHOICES = [
        (PHUC_VU, 'Nhân viên phục vụ'),
        (PHA_CHE, 'Nhân viên pha chế'),
        (KHO, 'Nhân viên kho'),
        (QUAN_LY, 'Quản lý'),
    ]
    NL = 'Nghỉ làm'
    DL = 'Đang làm'
    TT_CHOICES = [
        (NL, 'Nghỉ làm'),
        (DL, 'Đang làm'),
    ]
    manv = models.AutoField(primary_key=True) 
    hoten = models.CharField(max_length=30)
    ngaysinh = models.DateField()
    gioitinh = models.BooleanField(choices=GENDER_CHOICES, default=True)
    sdt = models.IntegerField()
    diachi = models.CharField(max_length=70)
    ngayvaolam = models.DateField()
    vitricongviec = models.CharField(
        max_length=30,
        choices=CV_CHOICES,
        default=PHUC_VU
    )
    trangthai = models.CharField(max_length=20, choices=TT_CHOICES, default=DL)

    class Meta:
        db_table = 'nhanvien'



class Thietbi(models.Model):
    TBPC = 'Thiết bị pha chế'
    TBQL = 'Thiết bị quản lý'
    TBLT = 'Thiết bị lưu trữ'
    T = 'Tốt'
    KT = 'Không tốt'
    LTB_CHOIES = [
        (TBPC, 'Thiết bị pha chế'),
        (TBQL, 'Thiết bị quản lý'),
        (TBLT, 'Thiết bị lưu trữ'),
    ]
    TT_CHOIES = [
        (T, 'Tốt'), 
        (KT, 'Không tốt'),
    ]
    matb = models.AutoField(max_length=10, primary_key=True)
    tentb = models.CharField(max_length=50)
    loaitb = models.CharField(max_length=20, choices=LTB_CHOIES, default=TBPC)
    soluong =models.FloatField()
    tinhtrang =models.CharField(max_length=20, choices=TT_CHOIES, default=T)
    ngaymua =models.DateField()
    giamua=models.FloatField()
    tonggia=models.FloatField(max_length=30)
    class Meta:
        db_table = 'thietbi'
    def save(self, *args, **kwargs):
        if self.soluong is not None and self.giamua is not None:
            self.tonggia = self.soluong * self.giamua
        else:
            self.tonggia = 0  

        super().save(*args, **kwargs)
class Baotri(models.Model):
    mabt = models.AutoField(max_length=10, primary_key=True)
    matb = models.ForeignKey('Thietbi', on_delete=models.CASCADE, db_column='matb')
    ngaybt=models.DateField()
    mota =models.CharField(max_length=100)
    chiphi=models.FloatField()
    nguoithuchien=models.CharField(max_length=50)
    class Meta:
        db_table = 'baotri'

class Dungcu(models.Model):
    CAI = 'Cái'
    BICH = 'Bịch'
    KG = 'KG'

    DVT_CHOIES = [
        (CAI, 'Cái'),
        (BICH, 'Bịch'),
        (KG, 'KG'),
    ]
    madc = models.AutoField(max_length=10, primary_key=True)
    tendc = models.CharField(max_length=50)
    soluong =models.IntegerField()
    dvt = models.CharField(max_length=20, choices=DVT_CHOIES, default=CAI)
    ngaymua=models.DateField()
    giamua=models.FloatField()
    tonggia = models.FloatField(max_length=30)
    class Meta:
        db_table = 'dungcu'
    def save(self, *args, **kwargs):
        if self.soluong is not None and self.giamua is not None:
            self.tonggia = self.soluong * self.giamua
        else:
            self.tonggia = 0  

        super().save(*args, **kwargs)

class Thongtinnguyenlieu(models.Model):
    CAI = 'Cái'
    KG = 'KG'
    BICH= 'Bịch'
    DVT_CHOIES = [
        (CAI, 'Cái'),
        (KG, 'KG'),
        (BICH, 'Bịch'),
    ]
    manl = models.AutoField(max_length=10, primary_key=True)
    tennl = models.CharField(max_length=30)
    dvt = models.CharField(max_length=10, choices=DVT_CHOIES, default=CAI)
    soluong = models.FloatField()
    gia = models.FloatField()
    ngayhethan = models.DateField()
    tonggia = models.FloatField(max_length=30)
    class Meta:
        db_table = 'nguyenlieu'
    def save(self, *args, **kwargs):
        if self.soluong is not None and self.gia is not None:
            self.tonggia = self.soluong * self.gia
        else:
            self.tonggia = 0  

        super().save(*args, **kwargs)
        


class LichSuThaoTac(models.Model):
    LOAI_THAO_TAC_CHOICES = [
        ('ADD', 'Thêm'),
        ('EDIT', 'Sửa'),
        ('DELETE', 'Xóa'),
    ]
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    loai_thao_tac = models.CharField(max_length=6, choices=LOAI_THAO_TAC_CHOICES)
    noi_dung = models.TextField()
    ngay_thuc_hien = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'lich_su_thao_tac'