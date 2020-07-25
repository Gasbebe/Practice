# Trajectory

## 사전지식

- 간단한 미적분
- 삼각함수
- 벡터

---

초기속도를 v로 각도 angle 만큼 출발하는 포물선

- v cos 
- v sin

---

위치의 단위는 m, 속도의 단위는 m/s(초당 몇 m을 움직였는지)

가속도의 단위는 m/s *s (초당 얼마만큼 속도가 변하는지)

---

**위치**를 시간에 대해서 `미분`하면 **속도**가 되고,

**속도**를 시간에 대해서 `미분`하면 **가속도**가 되고

**가속도**를 시간에 대해서 `적분`하면 **속도**가 되고

 **속도**를 시간에 대해서 `적분`하면 **위치**가 됩니다

---

x방향의 운동은 등속도 운동이다

a가속도, v속도, s위치
$$
x = v_0Cos\theta t
$$


---

y방향읜 운동은 중력에 의한 등가속도 운동
$$
y = -9.81/2 * t^2 + v_0Sin\theta t
$$

---

$$
t = 1/v_0Cos\theta * x
$$

---

$$
y = -9.81/2 * t^2 + v_0Sin\theta t
$$

---

$$
x = v_0^2Cos^2\theta * 2tan\theta /9.81
$$

---

만들 수식

- 속도 고정
- 시작지점
- 도착지점

---
- x = Vx * t
- **Vx = x / t**
- y = Vy0 * t - 1/2 * g * t *t
- y + 1/2 * g * t * t = Vy0 * t
- **Vy0 = y/t + 1/2 * g* t**

---

목표 위치로 떨어질 때까지 기본적인 발사체 공식은 두 방적식으로 나누어 집니다.

- 수평 거리 방정식(X 거리와 수평 거리에 대한 힘인 방정식)   **x = Vx * t**, 축 방정식은 초기 속도 시간, x 시간과 같습니다,
  - 초기 속도를 검색 할 수있는 거리를 이미 알고 있으므로, 속도를 구하는 방정식을 다음과 같이 쓸 수 있습니다.  **Vx = x / t**,  x의 방향 속도와 x 방향의 거리를
- 수직 거리 방정식 은 y = Vy0 * t - 1/2 * g * t *t  이고 
  - **Vy0 = y/t + 1/2 *g * t** 이다

---

```c#
public class Test{
    
    void Start(){
        cam = Camera.main;
    }
    
    void LaucherProjecttile(){
        Ray camRay = cam.ScreeenPointToRay(Input.mousePosition);
        RayCastHit hit;
        
        if(Physics.Raycast(camRay, out hit, 100f,layer)){
        	cursor.SetActive(true);
            cursor.transform.position = hit.point + Vector.up * 0.1f;
            
            Vector3 Vo = CalculateVelcoity(hit.point, tranform.position, 1f);
            //
            Rigidbody obj = Instantiate(bullet, shootPoint.position, Quaternion.identity);
            obj.velocity = Vo;
        }
    }
    //이 방법은 목표 벡터와 원점의 시작점이 필요합니다.
    //time : 비행시간
    Vector3 CalculateVelcoity(Vector3 target, Vector3 origin, float time){
        //define the distance x and y first
        Vector3 distanceY = target - origin;
        Vector3 distanceXZ = distance; //x와z의 평면이면 기본적으로 거리와 같은 벡터
        distanceXZ.y = 0f;//y는 0으로 설정
        
        //create a float the represent our distance
        float Sy = distance.y;//세로 높이의 거리를 지정
        float Sxz = distanceXZ.magnitude;
        
        //속도 계산
        float Vx = Sxz / time;
        float Vy = Sy / time * 0.5f * Mathf.Abs(Physics*gravity.y) * time;
        
        //계산으로 인해 두축의 초기 속도 가지고 새로운 벡터를 만들수 있음
        Vector3 result = distanceXZ.normalized;
        result *= Vxz;
        result.y = Vy;
        return result;
    }
    
    void setTrajectoryPoints(Vector3 pStartPosition , Vector3 pVelocity)
    {
        float velocity = Mathf.Sqrt((pVelocity.x * pVelocity.x) + (pVelocity.y * pVelocity.y));
        float angle = Mathf.Rad2Deg*(Mathf.Atan2(pVelocity.y , pVelocity.x));
        float fTime = 0;
        
        fTime += 0.1f;
        for (int i = 0 ; i < numOfTrajectoryPoints ; i++)
        {
            float dx = velocity * fTime * Mathf.Cos(angle * Mathf.Deg2Rad);
            float dy = velocity * fTime * Mathf.Sin(angle * Mathf.Deg2Rad) - (Physics2D.gravity.magnitude * fTime * fTime / 2.0f);
            Vector3 pos = new Vector3(pStartPosition.x + dx , pStartPosition.y + dy ,2);
            trajectoryPoints[i].transform.position = pos;
            trajectoryPoints[i].renderer.enabled = true;
            trajectoryPoints[i].transform.eulerAngles = new Vector3(0,0,Mathf.Atan2(pVelocity.y - (Physics.gravity.magnitude)*fTime,pVelocity.x)*Mathf.Rad2Deg);
            fTime += 0.1f;
        }
    }
}
```

