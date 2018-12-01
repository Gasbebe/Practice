메쉬 클래스에서

모든 정점은 하나의 배열의 저장되어 있다.

전체 tris 정수들로 이루어진 하나의 긴 베열에 저장된다 이배열은 3개마다 하나의 삼각형으로 그룹하 되어 있다, 0,1,2는 첫번째 삼각형, 3,4,5는 두번째 삼각형으로 이루어지는 형식이다



# 1. Quad Generator

```c#
namespace ProceduralModeling {

	public class Quad : ProceduralModelingBase {

		[SerializeField, Range(0.1f, 10f)] protected float size = 1f;

		protected override Mesh Build() {
			var mesh = new Mesh();

			//quad 크기
			var hsize = size * 0.5f; 

			// Quad 정점 좌표 정의
			var vertices = new Vector3[] {
				new Vector3(-hsize,  hsize, 0f), // 0  왼쪽 상단
				new Vector3( hsize,  hsize, 0f), // 1  오른쪽 상단
				new Vector3( hsize, -hsize, 0f), // 2  오르쪽 하단
				new Vector3(-hsize, -hsize, 0f)  // 3  왼쪽 하단
			};

			// Quad의 uv좌표
			var uv = new Vector2[] {
				new Vector2(0f, 0f), // 0번 정점의 uv좌표
				new Vector2(1f, 0f), // 1번 정점의 uv좌표
				new Vector2(1f, 1f), // 2번 정점의 uv좌표
				new Vector2(0f, 1f)  // 3번 정점의 uv좌표
			};

			// Quad의 법선 데이터
			var normals = new Vector3[] {
				new Vector3(0f, 0f, -1f), // 0번 정점의 법선
				new Vector3(0f, 0f, -1f), // 1번 정점의 법선
				new Vector3(0f, 0f, -1f), // 2번 정점의 법선
				new Vector3(0f, 0f, -1f)  // 3번 정점의 법선
			};

			//Quad의 면데이터 네 개의 버텍스로 이루어진 두 삼각형에 필요한 index를
            //삼각형 순서댈로 2개씩 나라히 놓는다
			var triangles = new int[] {
				0, 1, 2, // 1번 삼각형
				2, 3, 0  // 2번 삼각형
			};

			mesh.vertices = vertices;
			mesh.uv = uv;
			mesh.normals = normals;
			mesh.triangles = triangles;

			//만들어지 메쉬의 경계영역(bounds)을 계산한다 (culling에 필요)
			mesh.RecalculateBounds();

			return mesh;
		}

	}

}
```



# 2. Plane Generator

```c#
namespace ProceduralModeling {

	public class Plane : ProceduralModelingBase {

		// Plane 너비(widthSegments) 높이(heightSegments) 정점의 갯수
		[SerializeField, Range(2, 30)] protected int widthSegments = 8, heightSegments = 8;

		// Plane 크기
		[SerializeField, Range(0.1f, 10f)] protected float width = 1f, height = 1f;

		protected override Mesh Build() {
			var mesh = new Mesh();

			var vertices = new List<Vector3>();
			var uv = new List<Vector2>();
			var normals = new List<Vector3>();

			//격자상에 정점을 배열할 위치의 비율(00. ~ 1.0)을 산출하기 위한 행열수의 역수
			var winv = 1f / (widthSegments - 1);
			var hinv = 1f / (heightSegments - 1);

			for(int y = 0; y < heightSegments; y++) {
				//행의 위치 비율 (0.0 ~ 1.0)
				var ry = y * hinv;

				for(int x = 0; x < widthSegments; x++) {
					//열의 위치 비율(0.0 ~ 1.0)
					var rx = x * winv;

					vertices.Add(new Vector3(
						(rx - 0.5f) * width, 
						0f,
						(0.5f - ry) * height
					));
                    //정점의 갯수 비율에 따른 uv좌표 설정
					uv.Add(new Vector2(rx, ry));
                    //법선 방향 설정
					normals.Add(new Vector3(0f, 1f, 0f));
				}
			}

			var triangles = new List<int>();
			//너비와 높이따른 삼각형 갯수 계산  기본적으론 2개의 삼각형 추가
			for(int y = 0; y < heightSegments - 1; y++) {
				for(int x = 0; x < widthSegments - 1; x++) {
					int index = y * widthSegments + x;
					var a = index;
					var b = index + 1;
					var c = index + 1 + widthSegments;
					var d = index + widthSegments;
					
                    //첫번째 삼각형
					triangles.Add(a);
					triangles.Add(b);
					triangles.Add(c);
					
                    //두번째 삼각형
					triangles.Add(c);
					triangles.Add(d);
					triangles.Add(a);
				}
			}

			mesh.vertices = vertices.ToArray();
			mesh.uv = uv.ToArray();
			mesh.normals = normals.ToArray();
			mesh.triangles = triangles.ToArray();

			mesh.RecalculateBounds();

			return mesh;
		}

	}

}
```

