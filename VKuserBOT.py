import vk_api
import sys
import time

#253181870 = максим
#617288051
#551510928 # type: int

user_id = []
idu = []


def load_accs():   
        tok = []
        file = open(sys.path[0] + '/tokenVK.txt', 'r',encoding = 'utf-8-sig').readlines()
        for q in file:
        
            try:
                q = q.strip()
                tmp = q.split(':',1)
                idu.append(tmp[0])
                tok.append([bytes(tmp[1].strip(), 'UTF-8') ])
               
                
                print('загружен', tmp[0])
            except:
                print('не удалось загрузить аккаунт, array=',tmp)
        
        return tok 
go= load_accs()

def check():
        xui=[]
        for i in go:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.account.getInfo(fields = 'country')
                ada = d.account.getProfileInfo() 
                xui.append(i)       
            except vk_api.exceptions.ApiError:
                print('Неверный access_token. Возможно, аккаунт забанен, array =','[ id:',ada['id'],']')
        print('загружено', len(xui), 'аккаунтов')
        return xui
hu  = check()

def accs():
    iu = int(input('кому отправляем?(id): '))
    mes = input('введите сообщение: ')
    for i in hu:
        try:
            d = vk_api.VkApi(token=i).get_api()
            d.messages.send(user_id=iu,message=mes,random_id=0)
            ada = d.account.getProfileInfo()
            print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] отправил сообщение')
            
        except vk_api.exceptions.ApiError: 
            ada = d.account.getProfileInfo()
            print('сообщение не отправлено. Вероятно, проблемы с капчей или у пользователя закрыты сообщения, array =','[ id:',ada['id'],']')
            
       
    answ()

def whacs():
    try:
        iu = int(input('кому отправляем?(id): '))
        ha = int(input('сколько циклов?: '))
        mes = input('введите сообщение: ')
    except:
        print('нужно число!')
        whacs()
    g = 0
    while(g!=ha):
        g+=1
        for i in hu:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.messages.send(user_id=iu,message=mes,random_id=0)
                ada = d.account.getProfileInfo()
                print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] отправил сообщение')
            except vk_api.exceptions.ApiError: 
                ada = d.account.getProfileInfo()
                print('сообщение не отправлено. Вероятно, проблемы с капчей или у пользователя закрыты сообщения, array =','[ id:',ada['id'],']')
                
    answ()
                   
def like():
    try:
        hk = int(input('id кого лайкаем: '))
        ja = int(input('id записи: '))
    except:
        print('нужно число!')
        like()
    try:
        for i in hu:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.likes.add(type = 'comment',owner_id = hk,item_id = ja)
                ada = d.account.getProfileInfo()
                print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] поставил лайк')
            except vk_api.exceptions.ApiError:    
                    try:
                        d = vk_api.VkApi(token=i).get_api()
                        ada = d.account.getProfileInfo()
                        d.likes.add(type = 'photo',owner_id = hk,item_id = ja)
                        print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] поставил лайк')
                    except vk_api.exceptions.ApiError: 
                        ada = d.account.getProfileInfo()
                        print('невозможно поставить лайк. Вероятно, проблемы с капчей, array =','[ id:',ada['id'],']') 
             
    except:
        pass  
    answ()
   
def post():
    try:
        pasda = int(input('id у кого публикуем: '))
        dafa = input('публикуемый текст: ')
    except:
        print('нужно число!')
        post()
   
    for i in hu:
        try:
            d = vk_api.VkApi(token=i).get_api()
            d.wall.post(owner_id = pasda,message=dafa)
            ada = d.account.getProfileInfo()
            print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] опубликовал запись')
        except vk_api.exceptions.ApiError: 
            ada = d.account.getProfileInfo()
            print('невозможно опубликовать запись. Вероятно, у пользователя закрыта стена, array =', '[ id:',ada['id'],']')
                
    
    answ()

def wall():
    try:
        ga = int(input('кого комментим?(id):'))
        kas = int(input('id поста:'))
        fads = input('cообщение:')
    except:
        print('нужно число!')
        return wall()
    try:
        for i in hu:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.wall.createComment(owner_id = ga,post_id = kas, message = fads )
                ada = d.account.getProfileInfo()
                print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] оставил комментарий')
            except vk_api.exceptions.ApiError: 
                try:
                    d = vk_api.VkApi(token=i).get_api()
                    d.video.createComment(owner_id = ga,video_id = kas,message = fads)
                    ada = d.account.getProfileInfo()
                    print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] оставил комментарий')
                except vk_api.exceptions.ApiError:
                    try:
                        d = vk_api.VkApi(token=i).get_api()
                        d.photos.createComment(owner_id = ga,photo_id = kas,message = fads)
                        ada = d.account.getProfileInfo()
                        print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] оставил комментарий')
                    except vk_api.exceptions.ApiError:
                        ada = d.account.getProfileInfo()
                        print('невозможно оставить коммент. Возможно, у поста закрыты комментарии, array =','[ id:',ada['id'],']')
                        
    except:
        pass
            
    answ()
def group():
    try:
        gd = int(input('id группы: '))
    except:
        print('Нужно число!')
        group()
    for i in hu:
            try:
                d = vk_api.VkApi(token=i).get_api()
                d.groups.join(group_id = gd)
                ada = d.account.getProfileInfo()
                print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] вступил в группу')
            except vk_api.exceptions.ApiError:
                ada = d.account.getProfileInfo()
                print('акк не смог вступить в группу, array = ','[ id:',ada['id'],']')
    answ()

def friends_add():
    try:
        usd = int(input('id пользователя: '))
    except:
        print('нужно число!')
        friends_add()
    for i in hu:
        try:
            d = vk_api.VkApi(token=i).get_api()
            d.friends.add(user_id = usd)
            ada = d.account.getProfileInfo()
            print(ada['first_name'],ada['last_name'],'[ id:',ada['id'],'] добавился в друзья')
        except vk_api.exceptions.ApiError:
            ada = d.account.getProfileInfo()
            print('акк не смог добавиться в друзья, array =', '[ id:',ada['id'],']')
    answ()

def inf():
    try:
        use = int(input('id пользователя: '))
    except:
        print('нужно число!')
        inf()
    try:
        for i in hu:
            d = vk_api.VkApi(token=i[0]).get_api()
            suka = d.users.get(user_id = use)
        print(suka)
    except:
        pass
    answ()

def answ():
    print('h - справка по модам, re - реконнект акков')
    gogo = ('''
моды:
1 - отправка сообщений
2 - комментирование записей
3 - поставить лайк
4 - инфа о акке
5 - оставление записей на стене
6 - вступление в группу
7 - добавление в друзья
q - выход
    ''')
    a = input('>>')
    if a == 'h':
        print(gogo)
        answ()

    if a == '1':
        d = input('делаем в цикле?(y/n): ')
        if d == 'n':
            accs()
        if d == 'y':
            whacs()
    if a == '2':
        wall()
    if a == '3':
        like()
    if a == '4':
        inf()
    if a == '5':
        post()
    if a == '6':
        group()
    if a == '7':
        friends_add()
    if a == 're':   
        load_accs()
        check()  
    if a == 'q':
        exit(0)
    else:
        answ()


print('')
answ()
