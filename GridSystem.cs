using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GridSystem : MonoBehaviour
{
    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}

public class Grid {
    private int width;
    private int height;
    private float cellSizle;
    private Vector3 originPosition;
    private int [,] gridArray;

    public Grid(int width, int height, float cellSizle, Vector3 originPosition){

        this.width = width;
        this.height = height;
        this.cellSizle = cellSizle;
        this.originPosition = originPosition;

        gridArray = new int[width, height];

        for(int x = 0; x < gridArray.getLength(0); x++ ){
            for(int y = 0; y < gridArray.getLength(1); y++){
                //Debug.DrawLine()
            }
        
        }
    }

    private Vector3 GetWorldPosition(int x, int y){
        return new Vector3(x, y) * cellSizle + originPosition;
    }

    private GetXY(Vector3 worldPosition, out int x, out int y){
        x = Mathf.FloorToInt((worldPosition - originPosition).x / cellSizle);
        y = Mathf.FloorToInt((worldPosition - originPosition).y / cellSizle);
    }

    public void SetValue(int x, int y, int value){
        if(x >= 0 && y >= 0 && x < width && y < height){
            gridArray[x, y] = value;
            //String s = gridArray[x, y].ToString();
        }
    }

    public void SetValue(Vector3 worldPosition, int value){
        int x, y;
        GetXY(worldPosition, out x, out y);
        SetValue(x, y, value);
    }

    public int GetValue(int x, int y){
        if(x >= 0 && y >= 0 && x < width && y < height){
            return gridArray[x, y];
        }else{
            return 0;
        }
    }
    
    public int GetValue(Vector3 worldPosition){
        int x;
        int y;

        GetXY(worldPosition, out x, out y);
        return GetValue(x, y);
    }
}

public class Testing : MonoBehaviour{

}