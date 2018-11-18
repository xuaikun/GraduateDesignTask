#include <iostream>
#include <stdlib.h>
#include <time.h>
#include <algorithm>
#define N 1004
#include <ctime>
#include <fstream>
using namespace std;

int SelectSort(int *A, int n);				//¶¨ÒåÒ»¸öÅÅÐòº¯Êý 

struct {									//¸Ð¾õ½á¹¹Ìå±È½ÏÊÊºÏ~ 
	int EdgeList;							//ÎÞÏßÍ¼µÄ±ß 
	int EdgeList_New;							//ÎÞÏßÍ¼µÄ±ß 
	int Max_Common_Neighbor;				//ÊýÁ¿×î´óµÄCommon_Neighbor 
	int Common_Neighbor;					//¼ÆËãÃ¿Ìõ±ßµÄCommon_NeighborÊýÁ¿ 
	int Common_Neighbor_New;				//½«Common_NeighborÊýÁ¿Í³¼Æµ½ÉÏÈý½Ç¾ØÕóÖÐ 
	int Edge_Delete;						//Ã»ÓÃÉÏ  Í³¼Æ±»É¾³ýµÄ±ß 
	 
}Clique[N][N];						    	//¶þÎ¬¾ØÕó½á¹¹Ìå 

int main()
{
go_on:
	ifstream in;//¶¨Òå¶ÁÈ¡ÎÄ¼þÁ÷£¬Ïà¶ÔÓÚ³ÌÐòÀ´ËµÊÇin  ÎªÉ¶´ò¿ªÁ½´ÎÎÄ¼þ£¬µÚÒ»´Î´ò¿ªÊÇÎªÁËÖªµÀ Õâ¸öÁÚ½Ó¾ØÕóµÄnÎª¶àÉÙ 
	in.open("what.txt");//´ò¿ªÎÄ¼þ
	
	srand((unsigned)time(0));
	int n;                                //¶¨Òå½Úµã¸öÊý 
	clock_t start, finish;
	int Clique_Count = 0;				  // ·ÖÍÅ¸öÊý 
	                  
	string str;
	getline(in, str);
	cout << "length of str =" << str.length() << endl;
	
	n = (str.length()+1)/2;					 //ÊäÈë½Úµã¸öÊý  ÒòÎªÃ¿Á½¸öÊý×ÖÖ®¼ä»áÓÐÒ»¸ö¿Õ¸ñ£¬½«¿Õ¸ñµÄÊýÁ¿¼õµô 
	
	cout << "length of n =" << n << endl;	
	int Node[n];                  
	       //ÓÃÓÚ¼ìÑéÄ³¸ö½ÚµãÊÇ·ñÃ»ÓÐ¼ÓÈëÄ³¸öÍÅ 
	int NodeList[n][n];                 //¼ì²é½Úµã¶¼½øÈëÁËÄÄ¸öNodeList£¬¼ÇÂ¼Éú³ÉÁË¼¸¸öNodeList 
	int Node_New[n];
	int NodeList_New[n][n];
	
	int First[n];						//¶¨ÒåÁ½¸öÖÐ¼ä¼ÆËã¾ØÕó ÓëÊ¦½ãÒ»Ñù~ 
	int Second[n];
	
	int Common_Neighbor_Sort[n];		//Common_NeighborÅÅÐò
	int Degree[n];						//Í³¼ÆÃ¿¸ö½ÚµãµÄ¶È 
	int Degree_Inceasing_Order[n];		//°Ñ¶È¸øÅÅÐò
	 
	int max_Degree_Inceasing_Order = 1; //Ã¿´Î¶¼ÐèÒª °ÑÃ¿¸ö½Úµã¶ÈÅÅÐòÖÐµÄ×î´óÖµÄÃ³öÀ´ £¬*********** 
										//½«max_Degree_Inceasing_Order = 0×÷ÎªwhileÑ­»·ÖÕÖ¹µÄÌõ¼þ 
										//max_Degree_Inceasing_Order = 0 ÒâÎ¶×ÅÃ¿¸öµã¶¼²»ÔÚÏàÁ¬,¿ÉÒÔ½áÊø²éÑ¯ 
	
	int Max_Degree = 0;					//µ±Common_NeighborÊýÁ¿×î´óµã²»Ö¹Á½¸öÊ±£¬ÐèÒªÕÒ³öµ±Ä³Ç°Á½¸ö½ÚµãµÄ×î´ó¶È 
	int Min_Edge  = 10000;				//µ±Common_NeighborÊýÁ¿×î´óµã²»Ö¹Á½¸öÊ±£¬ÐèÒªÕÒ³öµ±Ç°Ä³Á½¸ö½ÚµãÉ¾³ýµÄ±ßµÄÊýÁ¿×îÉÙ 
	for(int i = 1; i <= n; i++)          //³õÊ¼»¯½Úµã 
	{
		Node[i]        = 1;               //È·±£Ã¿¸ö½Úµã¶¼´æÔÚ  Node[i] == 1Ê±±íÊ¾´æÔÚ´Ë½Úµã£¬·ñÔò±íÊ¾²»´æÔÚ 
		NodeList[i][1] = i;               //È·±£³õÊ¼»¯Ê±Ã¿¸ö½Úµã´æÔÚÓÚÒ»¸öCliqueÖÐ
		for(int j = 2; j <= n; j++)      //Ã¿¸öNodeList³õÊ¼»¯Ê±Ö»ÓÐNodeList[i][1] = 1£¬j != 1Ê± NodeList[i][j] = 0; 
		{								//Èôi½Úµã±»¼ÓÈëµ½Ä³¸öCliqueÖÐ£¬ÄÇÃ´ NodeList[i][1] = 0; 
			NodeList[i][j] = 0;			//i=1 to i->n Ñ­»·Í³¼ÆNodeList[i][1] ÖÐµÈÓÚ 1µÄ¸öÊý ¾ÍÊÇCliqueµÄ¸öÊý 
		} 
 	}
	in.close();//¶ÁÈ¡Íê³ÉÖ®ºó¹Ø±ÕÎÄ¼þ
	
	
	/*´ÓÕâÀï¿ªÊ¼¸³ÖµÁÚ½Ó¾ØÕó*/ 
	ifstream infile;//¶¨Òå¶ÁÈ¡ÎÄ¼þÁ÷£¬Ïà¶ÔÓÚ³ÌÐòÀ´ËµÊÇin  	// ÎÞÏòÍ¼´ÓÎÄ¼þÖÐ¶ÁÈ¡ÁÚ½Ó¾ØÕó±íÊ¾
	infile.open("ok.txt");//´ò¿ªÎÄ¼þ
	for (int i = 1; i <= n; i++)//¶¨ÒåÐÐÑ­»·
	{
		for (int j = 1; j <= n; j++)//¶¨ÒåÁÐÑ­»·
		{
			infile >> Clique[i][j].EdgeList;//¶ÁÈ¡Ò»¸öÖµ£¨¿Õ¸ñ¡¢ÖÆ±í·û¡¢»»ÐÐ¸ô¿ª£©¾ÍÐ´Èëµ½¾ØÕóÖÐ£¬ÐÐÁÐ²»¶ÏÑ­»·½øÐÐ
		}
	}
	infile.close();//¶ÁÈ¡Íê³ÉÖ®ºó¹Ø±ÕÎÄ¼þ

	for(int i = 1; i <= n; i++)
	{
		for(int j = 1; j <= n; j++)
		{
			cout << Clique[i][j].EdgeList << " ";
			if(j == 5)
			{
				cout << endl;
			}
		}
	}

	for(int i = 1; i <= n; i++)							//°ÑClique[i][j].EdgeListµÄ±¸·Ýµ½Clique[i][j].EdgeList_New 
	{													//±¸·ÝÊý¾Ý 
		Node_New[i] = Node[i];
		for(int j = 1; j <= n; j++)
		{
			Clique[i][j].EdgeList_New = Clique[i][j].EdgeList;
			NodeList_New[i][j]  = NodeList[i][j];
		}
	}
	start = clock();									//¿ªÊ¼¼ÆÊ± 
end1:
	
	while(max_Degree_Inceasing_Order)					// max_Degree_Inceasing_Order = 0 ×÷Îª³ÌÐòÍ£Ö¹µÄ±êÖ¾£¬
														// max_Degree_Inceasing_Order ½Úµã¶ÈÅÅÐòºóµÄ×î´óÖµ ×î´óÖµÎª0 ±íÃ÷Ã¿¸ö½Úµã²»ÏàÁ¬£¬
														//ÔòÈ«²¿µãÒÑ¾­È«²¿·Öµ½¸÷¸öClique 
	{
		
Step1_1:
		for(int i =1; i <= n; i++)
		{
			Common_Neighbor_Sort[i] = 0;	
		} 
	
		Max_Degree = 0;                                //Îª·ÀÖ¹ÉÏ´ÎÁ½¸ö½Úµã¶ÈµÄÓ°Ïì£¬×î´ó¶ÈÃ¿´Î¶¼µÃ¸üÐÂ 
		 
		for(int i = 1; i <= n; i++)	                   //±£Ö¤i < j   // ¼ÆËãÈôÑ¡ÖÐÕâÁ½¸öµãºóÐèÒªÉ¾³ýµÄ±ßµÄÊýÁ¿ 
		{
			for(int j = 1; j <= n; j++)
			{
				First[j] = Clique[i][j].EdgeList; 
			}
			for(int k = i + 1; k <= n; k++)
			{
				if(Clique[i][k].EdgeList == 1)					//±£Ö¤ÕâÁ½¸öµãÊÇÏàÁ¬µÄ£¬´æÔÚedge(i,j) 
				{
					int num = 0;								//ÐèÒªÉ¾³ýµÄ±ß 
					for(int u = 1; u <= n; u++)
					{
						Second[u] = Clique[k][u].EdgeList;
					}
					for(int q = 1; q <= n; q++)
					{
						if(First[q] != Second[q] && First[q] != 0)	//±£Ö¤½öÓë½ÏÐ¡µãiÏàÁ¬£¬¸ÃÉ¾³ý 
						{
							num = num + 1; 							//Ê±¿Ì¼ÇµÃÕâÑùµÄÇé¿ö
																	//0 0 1 
																	//0 0 0
																	//1 0 0 
						}
					}
					for(int c = 1; c <= n; c++)
					{
						if(Clique[k][c].EdgeList != 0)			//¶ÔÓÚÐèÒªÉ¾³ýÓëjÏàÁ¬µÄ±ß 
						{
							num = num + 1;
						}
					}
					Clique[i][k].Edge_Delete = num - 1;							//ÎªÊ²Ã´Òª¼õ1£¿ ±¾ÉíÎª1£¬µ«¶Ô·½¶ÔÓ¦²»Îª1£¬¶à¼ÓÁË1Ìõ±ß£¬ËùÒÔ¼õ1 
					Clique[k][i].Edge_Delete = Clique[i][k].Edge_Delete;		//ÆäÊµÊÇÍ¬Ò»Ìõ±ß£¬É¾³ýµÄ±ßÊÇÒ»ÑùµÄ 
				}
				else{
					Clique[i][k].Edge_Delete = 0;
				} 
			}
		} 		
														// Í³¼ÆÃ¿¸ö½ÚµãµÄ¶È±£´æµ½Degree[],Êý×éÏÂ±í¼´Îª½ÚµãµÄ±êºÅ									
		for(int i = 1; i <= n; i++)
		{
			Degree[i] = 0;										//Ã¿¸ö½ÚµãµÄ¶È³õÊ¼»¯Îª0 
			for(int j = 1; j <= n; j++)
			{
				Degree[i] = Degree[i] + Clique[i][j].EdgeList; // Ã¿Ò»ÐÐµÄÖµµÄ×ÜºÍ¼´ÎªÄ³¸ö½ÚµãµÄ¶È 
			}	
			Degree_Inceasing_Order[i] = Degree[i];				//½«Degree[]µÄÖµÒÀ´Î´æÈëDegree_Increasing_Order[]ÓÃÓÚÅÅÐò
																//ÒÀ¾ÉÒª±£´æDegree²»±ä£¬·½±ã ¡°²éÑ¯Ê±½Úµã¡± Ê±Ê¹ÓÃ 
		} 
									//½«½ÚµãµÄ¶È½øÐÐÅÅÐò~ 
		SelectSort(Degree_Inceasing_Order, n);
		
		max_Degree_Inceasing_Order = Degree_Inceasing_Order[1];

		if(max_Degree_Inceasing_Order == 0)						//ÒÔ»ñÈ¡×î´ó½Úµã¶ÈÎª0£¬ÂíÉÏÖÕÖ¹³ÌÐò 
		{
			goto end1;
		} 
	
		/*¼ÆËãÃ¿Ìõ±ßµÄcommon neighborÊýÁ¿*/
		for(int i = 1; i <= n; i++)				
		{
			
			for(int j = 1; j <= n; j++)						//¿ØÖÆÐÐµÄ±ä»¯ 
			{
				First[j] = Clique[i][j].EdgeList;           //  ÌáÈ¡µÚiÐÐÔªËØ 
			
			}	
			
			for(int k = 1; k <= n; k++)						//¿ØÖÆÁÐµÄ±ä»¯
			{
			
				if(Clique[i][k].EdgeList == 1)				//±£Ö¤²Ù×÷µÄÁ½¸öµãÊÇÏàÁ¬µÄ 
				{
				
					for(int j = 1; j <= n; j++)			 
					{
						Second[j] = Clique[k][j].EdgeList;  //  ÌáÈ¡µÚkÐÐÔªËØ 
					}
				 
					int Diff = 0;								//ÁÚ¾Ó¼ÆÊý 	
					//int num = 0;								//ÐèÒªÉ¾³ýµÄ±ß
					for(int u = 1; u <= n; u++)
					{
						if(First[u] == Second[u] && First[u] != 0)			//ÏàÁ¬µÄÁ½¸öµã(edge) ÓÐ¹²Í¬µÄµã£¨Common_Neignbor£©,²¢ÇÒ0²»ËãÏàÁ¬ 
						{
								Diff = Diff + 1;
						}	
					}	
					Clique[i][k].Common_Neighbor = Diff;    //Ã¿Ìõ±ßµÄCommon_NeighborÊýÁ¿ 
				}
				else
					Clique[i][k].Common_Neighbor = 0;	
			}
		} 
		for(int i = 1; i <= n; i++)				//	Ö»»ñÈ¡Common_NeighborÉÏÈý½Ç²¿·ÖÊý¾Ý£¬±£Ö¤Common_Neighbor[][]Ö»±£´æ²»Í¬±ßµÄ¸öÊý 
		{
			for(int j = 1; j <= n; j++)
			{	
				if(i <= j)
				{
					Clique[i][j].Common_Neighbor_New = Clique[i][j].Common_Neighbor; //½«Common_NeighborµÄÉÏÈý½ÇÌáÈ¡³öÀ´ 
				} 
				if(j == n)
				{
				} 	
			}	
		} 

		/*******************************************************/
		/***********Common_Neighbor_Sort³öÁËÎÊÌâ****************/
		/*******************************************************/
		/*½«Ã¿Ò»¸ö½Úµã¶ÔÓ¦µÄ×î´óCommon_NeighborÕÒ³öÀ´*/
		for(int i = 1, j = 1; i <= n; i++)
		{														//*********************Ö®Ç°ÕâÀïºÃÏñ´íÁË***************************// 
			int max = Clique[i][i].Common_Neighbor_New;         //´Ó¶Ô½ÇÏß¿ªÊ¼  ~~~~~~~~~~~~²ÅÊÇÕýÈ·µÄ  Õâ¸öÖµµÈÓÚ0  ²»È»»á³öÏÖËæ»úÖµ 
			for(j = i; j <= n; j++)
			{
				if(max < Clique[i][j].Common_Neighbor_New)
				{ 
					max = Clique[i][j].Common_Neighbor_New;	//Èôµ±Ç°maxÖµ±È Clique.Common_Neighbor_New[i][j]Ð¡£¬ÔòÌæ»» maxÖµ 
				}
			}
			Common_Neighbor_Sort[i] = max;
		}
		
		SelectSort(Common_Neighbor_Sort, n);			//¶ÔÍ³¼Æ³öÀ´µÄÃ¿¸öµãµÄ×î´óCommon_NeighborÊýÁ¿½øÐÐÅÅÐò 
	
		/*Ê×ÏÈÕÒ³öCommon_Neighbor×î´óµÄ£¬ÈçCommon_Neighbor×î´óÖµÎ¨Ò»£¬Ôò¼ÌÐø£¬Èç×î´óÖµ²»Î¨Ò»ÔòÔÙ±È½Ï
		Degree[],ÓÐÏÞºÏ²¢¶È×î´óµÄÁ½¸ö½Úµã*/

		int Max_Common_Neighbor_num = 0; 					//Í³¼ÆÓÐÓÃ×î´óCommon_NeighborµÄ±ßµÄÊýÁ¿ 
		int Max_Common_Neighbor_i_Point[n];					//±£´æÃ¿Ìõ±ßµÄi½Úµã 
		int Max_Common_Neighbor_j_Point[n];					//±£´æÃ¿Ìõ±ßµÄj½Úµã 
		int Max_Common_Neighbor_i_Point_Last;				//µ±×î´óCommon_NeighborµÄ±ß²»Ö¹Ò»ÌõÊ±£¬ÐèÒªÕÒ¶È×î´óµÄÄÇÁ½¸ö½Úµã »ñÈ¡i½Úµã 
		int Max_Common_Neighbor_j_Point_Last;				//»ñÈ¡j½Úµã 
		int Max_i;											//×îÓÅµÄÁ½¸öµã~µÄ ±êºÅ 
		int Max_j;	
		Max_Common_Neighbor_num = 0;										//Ò»¶¨´æÔÚ Max_j > Max_i 
		
		for(int i = 1; i <= n; i++)
		{
			for(int j = i + 1; j <= n; j++)
			{
				// Common_NeighborÊýÁ¿×î´óµãÎª Common_Neighbor_Sort[1]  Ã¿´Î¶¼Ö»ÄÃ×î´óµÄ³öÀ´±È½Ï¼´¿É  
				if(Common_Neighbor_Sort[1] == Clique[i][j].Common_Neighbor_New && Clique[i][j].EdgeList != 0)	
				//ÕÒµ½×î´óCommon_NeighborµÄÁ½¸ö½Úµã ·ÀÖ¹×î´óCommon_NeighborÎª0Ê±³öÏÖ´íÎó£¬±£Ö¤Ñ¡ÖÐµÄÁ½¸ö½Úµã±ØÐëÏàÁ¬ 
				{
					Max_Common_Neighbor_num++;					 						//Í³¼Æ×î´óCommon_NeighborÊýÁ¿ 
					Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num] = i;			//Í³¼Æ×î´óCommon_NeighborÎ»ÖÃ ¼´£ºÁ½¸ö½Úµã±êºÅ 
					Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num] = j;			//Max_Common_Neighbor_num¿ÉÒÔ×÷Îªindex 
				}
			}	
		} 
		Max_Degree = 0;
		Min_Edge = 10000;
		if(Max_Common_Neighbor_num != 1)								//º¬ÓÐ×î´óCommon_NeighborµÄ±ß²»Ö¹Ò»Ìõ 
		{
			for(int k = Max_Common_Neighbor_num; k >= 1; k-- )		  //Í¨¹ýMax_Common_Neighbor_num×÷Îªindex½«ËüÃÇÒ»ÌõÌõÕÒ³öÀ´ 
			{														  //²¢°ÑÑ¡ÖÐ±ßÖÐ¶È×î´óµÄÕÒ³öÀ´ 
				int i = Max_Common_Neighbor_i_Point[k]; 
				int j = Max_Common_Neighbor_j_Point[k];
			/*ÕÒ³öÐèÒªÉ¾³ýµÄ±ß×îÉÙµÄÁ½¸öµã*/
			//Clique[i][j].Edge_Delete
				if(Min_Edge > Clique[i][j].Edge_Delete)
				{
					Min_Edge = Clique[i][j].Edge_Delete;
					Max_Common_Neighbor_i_Point_Last = i;
					Max_Common_Neighbor_j_Point_Last = j;
				}
			
			}
			Max_i =  Max_Common_Neighbor_i_Point_Last;					//ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄedge(i,j) 
			Max_j =  Max_Common_Neighbor_j_Point_Last; 
		} 
		else															//×î´óCommon_NeighborµÄ±ßÖ»ÓÐÒ»Ìõ 
		{

			Max_i = Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num]; //ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄµÄedge(i,j) 
			Max_j = Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num]; //Max_Common_Neighbor_num¾ÍÊÇindex 
		} //end Step1
Step2_1:
		{ 
		//¶ÔMax_i ºÍMax_j ½øÐÐ´¦Àí ¾ÍÊÇ¶ÔClique·ÖÍÅ½øÐÐ´¦Àí£¬Node[],NodeList[][]¶¼Òª½øÐÐ´¦Àí
		//Madx_i ºÍMax_j ±íÊ¾×î´óCommon_Neighbor ²¢ÓÐ×î´ó¶ÈµÄÁ½¸öÁ¬½Óµã edge(Max_i,Max_j)
		//Node[] == 1Ê±±íÊ¾Õâ¸öµãÎ´ÊÜµ½´¦Àí£¬Node[] == 0Ê±±íÊ¾ÒÑ¾­¼ÓÈëÄ³¸öClique
		//NodeList[i][1] == 1Ê±±íÊ¾ÕâÀïÓÐÒ»¸öClique NodeList[i][1] == 0Ê±±íÊ¾ÕâÀï²»´æÔÚClique  
		
		//Clique[Max_i][Max_j].EdgeList ÐèÒª±»´¦Àí 
		//´æÔÚÓÚClique[Max_i][]µ«²»´æÔÚÓëClique[Max_j][]ÖÐµÄµã¾ùÎª0 
		//Clique[Max_j][].EdgeListÈ«²¿Îª0
		
		//ÒÑ¾­µÃµ½ Max_i  Max_j Ä¿Ç°½ö¶ÔËüÃÇÁ½¸öµã½øÐÐ²Ù×÷  ************************ 
		
		//¶Ô¼ÓÈëCLique½øÐÐ´¦Àí  Ò»¶¨´æÔÚ Max_i < Max_j  
		int temp;
		if(Max_i > Max_j)										//ÈôMax_i½Ï´ó£¬Ôò»¥»»Max_iÓëMax_jµÄÖµ 
		{
			temp  = Max_j;
			Max_j = Max_i;
			Max_i = temp; 
		}
				
		NodeList[Max_j][1] = 0;							     //¼õÉÙÒ»¸öCLique
		Node[Max_j]		   = 0;					  	      	//¼õÉÙÒ»¸öNode ¾ù±íÊ¾½«Max_jÓëMax_iºÏ²¢ÎªMax_i 
		
															//±£´æÍ¬ÔÚÒ»¸öÍÅÀïÃæ  ¿¼ÂÇÒ»¸öÎÊÌâ~  
															//¾ÍÊÇµ±Ô­À´µÄMax_i > Max_j Ê±Òª°Ñ Max_i Óë Max_j»¥»»
															//NodeList[Max_j][i]µÄÖµÒ²µÃ±£´æµÄÒª±£´æµ½NodeList[Max_i][i]  
		{
			NodeList[Max_i][Max_j] = Max_j;					//Ö÷ÒªÊÇNodeList[Max_j][1] = Max_j 
			for(int i = 2; i <= n; i++)
			{
				if(NodeList[Max_j][i] != 0)					//½«ÊôÓÚNodeList[Max_j][i]¹é²¢µ½NodeList[Max_i][i]ÖÐ 
				{
					NodeList[Max_i][i] = i;
				}	
			}
		}		
		for(int i = 1; i <= n; i++)								//NodeList[Max_j][i]ÖÐµÄµãÒÑ¾­±»¹é²¢µ½NodeList[Max_i][i]ÁË£¬½«Nodelist[Max_j][i]ÇåÁã 
		{
			NodeList[Max_j][i] = 0;	
		}											

Step3_1:
		//¶Ô±ß½øÐÐ²Ù×÷ É¾³ý½öÓëMax_iµãÏàÁ¬µÄ±ß (Ê¦½ã½âÊÍµÄ£¬µÚÈý¸öµã½öÓëÆäÖÐÒ»¸öµãÏàÁ¬£¬ËüÃÇµÄ±ßÉ¾³ý)
		for(int j = 1; j <= n; j++)					     	//¿ØÖÆÐÐµÄ±ä»¯ 
		{
			First[j] = Clique[Max_i][j].EdgeList;         //  ÌáÈ¡µÚiÐÐÔªËØ 
			Second[j] = Clique[Max_j][j].EdgeList;       //  ÌáÈ¡µÚkÐÐÔªËØ 
		}	
		for(int u = 1; u <= n; u++)
		{												//ÒÑ¾­Ã÷È·Max_iºÍMax_jÊÇÏàÁ¬µÄ£¬²é¿´ËüÃÇ¶ÔÓ¦ÁÚ½Ó¾ØÕóµÄMax_iÐÐºÍMax_jÐÐ
														//¶ÔÓ¦ÁÐÊÇ·ñÏàµÈ£¬ÏàµÈÇÒµÈÓÚ1±íÊ¾µÚÈý¸öµãkÓëMax_i¡¢Max_jÏàÁ¬
														//ÔòEdge(Max_i,k)(Èç¹ûk>Max_iÊ± ÔòÎªEdge(k, Max_i))²»ÐèÒªÉ¾³ý£¬·´Ö®ÐèÒªÉ¾³ý 
			if(First[u] != Second[u] && First[u] == 1)	//´æÔÚÒ»¸öµã½öÓëÏàÁ¬µÄMax_iµãÏàÁ¬ ¼´ Clique[Max_i][u].EdgeList = 1;
			{
					Clique[Max_i][u].EdgeList = 0;		//Éú³ÉµÄÊÇÎÞÏòÍ¼£¬ÐèÒªÖÃ¶Ô³ÆµÄÁ½¸öÖµÎª0£¬¼´ÎªÉ¾³ý±ß 
					Clique[u][Max_i].EdgeList = 0;
			}			
		}
		// ½«Óë±êºÅ´óµÄµã¼´Max_jÏàÁ¬µÄ±ßÈ«²¿É¾µô	//ÕâÑù×öÉÙÁËÒ»Ð©¹¤×÷£¬±È½ÏºÃÀí½â£¬¿ÉÄÜÖ±½ÓËµ²»Í¨ 
		for(int i = 1; i <= n; i++)
		{
			Clique[Max_j][i].EdgeList = 0;			//Éú³ÉµÄÊÇÎÞÏòÍ¼£¬ÐèÒªÖÃ¶Ô³ÆµÄÁ½¸öÖµÎª0£¬¼´ÎªÉ¾³ý±ß 
			Clique[i][Max_j].EdgeList = 0;
		}
		
Step4_1:
				Max_i;									 	//Max_i ºÍ Max_j ºÏ²¢Îª Max_i 
		} 
Step5_1:
		/*ÓÉÓÚ½Úµã±»ÐÞ¸Ä£¬Ã¿¸ö½ÚµãµÄ¶ÈÒ²±»ÐÞ¸ÄÁË ÖØÐÂ¼ÆËã¶ÈµÄÖµ*/ 
			for(int i = 1; i <= n; i++)
			{
				Degree[i] = 0;										//Ã¿¸ö½ÚµãµÄ¶È³õÊ¼»¯Îª0 
				for(int j = 1; j <= n; j++)
				{
					Degree[i] = Degree[i] + Clique[i][j].EdgeList; // Ã¿Ò»ÐÐµÄÖµµÄ×ÜºÍ¼´ÎªÄ³¸ö½ÚµãµÄ¶È 
				}	
				Degree_Inceasing_Order[i] = Degree[i];				//½«Degree[]µÄÖµÒÀ´Î´æÈëDegree_Increasing_Order[]ÓÃÓÚÅÅÐò
																	//ÒÀ¾ÉÒª±£´æDegree²»±ä£¬·½±ã ¡°²éÑ¯Ê±½Úµã¡± Ê±Ê¹ÓÃ 
			} 										//½«½ÚµãµÄ¶È½øÐÐÅÅÐò~ 
			SelectSort(Degree_Inceasing_Order, n);
			
			max_Degree_Inceasing_Order = Degree_Inceasing_Order[1];

			for(int i = 1; i <= n; i++)	//±£Ö¤i < j   // ¼ÆËãÈôÑ¡ÖÐÕâÁ½¸öµãºóÐèÒªÉ¾³ýµÄ±ßµÄÊýÁ¿ 
			{
				for(int j = 1; j <= n; j++)
				{
					First[j] = Clique[i][j].EdgeList; 
				}
				for(int k = i + 1; k <= n; k++)
				{
					if(Clique[i][k].EdgeList == 1)					//±£Ö¤ÕâÁ½¸öµãÊÇÏàÁ¬µÄ£¬´æÔÚedge(i,j) 
					{
						int num = 0;								//ÐèÒªÉ¾³ýµÄ±ß 
						for(int u = 1; u <= n; u++)
						{
							Second[u] = Clique[k][u].EdgeList;
						}
						for(int q = 1; q <= n; q++)
						{
							if(First[q] != Second[q] && First[q] != 0)	//±£Ö¤½öÓë½ÏÐ¡µãiÏàÁ¬£¬¸ÃÉ¾³ý 
							{
								num = num + 1; 
							}
						}
						for(int c = 1; c <= n; c++)
						{
							if(Clique[k][c].EdgeList != 0)			//¶ÔÓÚÐèÒªÉ¾³ýÓëjÏàÁ¬µÄ±ß 
							{
								num = num + 1;
							}
						}
						Clique[i][k].Edge_Delete = num - 1; 
						Clique[k][i].Edge_Delete = Clique[i][k].Edge_Delete; //ÆäÊµÊÇÍ¬Ò»Ìõ±ß£¬É¾³ýµÄ±ßÊÇÒ»ÑùµÄ  
					}
					else{
						Clique[i][k].Edge_Delete = 0;
					} 
				}
			} 
			if(max_Degree_Inceasing_Order == 0)						//ÒÔ»ñÈ¡×î´ó½Úµã¶ÈÎª0£¬ÂíÉÏÖÕÖ¹³ÌÐò  Max_i ÒÑ¾­µ¥¶À´æÔÚ 
			{
				goto end1;
			}  	

			if(Degree[Max_i] == 0)					//Èç¹ûMax_i½Úµã¶ÀÁ¢ÁË£¬ÁíÑ¡Ò»Ìõ±ß¼´ÁíÍâÁ½¸öµã 
			{
				goto Step1_1;
			}
			else								    // »¹ÓÐÓëMax_iÏàÁ¬µÄ±ß 
			{
				/*¼ÆËã°üº¬Max_i½ÚµãµÄ±ßµÄCommon_NeighborµÄ×î´óÖµÇé¿ö*/	
				for(int j = 1; j <= n; j++)						//¿ØÖÆÐÐµÄ±ä»¯ 
				{
					First[j] = Clique[Max_i][j].EdgeList;           //  ÌáÈ¡µÚiÐÐÔªËØ 
				}	
				for(int k = 1; k <= n; k++)						//¿ØÖÆÁÐµÄ±ä»¯
				{
					if(Clique[Max_i][k].EdgeList == 1)				//±£Ö¤²Ù×÷µÄÁ½¸öµãÊÇÏàÁ¬µÄ 
					{
						for(int j = 1; j <= n; j++)			 
						{
							Second[j] = Clique[k][j].EdgeList;  //  ÌáÈ¡µÚkÐÐÔªËØ 
						}
						int Diff = 0;								//ÁÚ¾Ó¼ÆÊý 	
						for(int u = 1; u <= n; u++)
						{
							if(First[u] == Second[u] && First[u] != 0)			//ÏàÁ¬µÄÁ½¸öµã ÓÐ¹²Í¬µÄµã£¨Common_Neignbor£©,²¢ÇÒ0²»ËãÏàÁ¬ 
							{
									Diff = Diff + 1;
							}	
						}	
						Clique[Max_i][k].Common_Neighbor = Diff;    //Ã¿Ìõ±ßµÄCommon_NeighborÊýÁ¿ 
					}
					else
						Clique[Max_i][k].Common_Neighbor = 0;	
				}
				//	Ö»»ñÈ¡Common_NeighborÉÏÈý½Ç²¿·ÖÊý¾Ý£¬±£Ö¤Common_Neighbor[][]Ö»±£´æ²»Í¬±ßµÄ¸öÊý 
				for(int j = 1; j <= n; j++)						//²»ÖªµÀMax_i ºÍ jË­´óË­Ð¡ 
				{
					Clique[Max_i][j].Common_Neighbor_New = Clique[Max_i][j].Common_Neighbor; //½«Common_NeighborµÄÉÏÈý½ÇÌáÈ¡³öÀ´ 
				}	
	
				//ÒÑ¾­»ñµÃ Clique[Max_i][k].Common_Neighbor_New	
				int max = Clique[Max_i][1].Common_Neighbor_New; 
				for(int j = 2; j <= n; j++)
				{
					if(max < Clique[Max_i][j].Common_Neighbor_New)
					{ 
						max = Clique[Max_i][j].Common_Neighbor_New;	//Èôµ±Ç°maxÖµ±È Clique.Common_Neighbor_New[i][j]Ð¡£¬ÔòÌæ»» maxÖµ 
					}
				}
				Common_Neighbor_Sort[1] = max;
				//Common_Neighbor_Sort[Max_i] = max;					// Max_i×î´óµÄCommon_Neighbor Îª max 
				//×î´óµÄCommon_Neighbor = max
				//Á½¸ö¶¥µã·Ö±ðÎª Max_i Max_j ÅÐ¶Ïmax ÊÇ·ñÎ¨Ò»
				Max_Common_Neighbor_num = 0;
				for(int j = 1; j <= n; j++)
				{
					// Common_NeighborÊýÁ¿×î´óµãÎª Common_Neighbor_Sort[1]  Ã¿´Î¶¼Ö»ÄÃ×î´óµÄ³öÀ´±È½Ï¼´¿É  
					if(Common_Neighbor_Sort[1] == Clique[Max_i][j].Common_Neighbor_New && Clique[Max_i][j].EdgeList != 0)	
					//ÕÒµ½×î´óCommon_NeighborµÄÁ½¸ö½Úµã ·ÀÖ¹×î´óCommon_NeighborÎª0Ê±³öÏÖ´íÎó£¬±£Ö¤Ñ¡ÖÐµÄÁ½¸ö½Úµã±ØÐëÏàÁ¬ 
					{
						Max_Common_Neighbor_num++;					 						//Í³¼Æ×î´óCommon_NeighborÊýÁ¿ 
						//Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num] = Max_i;			//Í³¼Æ×î´óCommon_NeighborÎ»ÖÃ ¼´£ºÁ½¸ö½Úµã±êºÅ 
						Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num] = j;			//Max_Common_Neighbor_num¿ÉÒÔ×÷Îªindex 
					}
				}	
				Max_Degree = 0;
				Min_Edge   = 10000;
				if(Max_Common_Neighbor_num != 1)								//º¬ÓÐ×î´óCommon_NeighborµÄ±ß²»Ö¹Ò»Ìõ 
				{
					for(int k = Max_Common_Neighbor_num; k >= 1; k-- )		  //Í¨¹ýMax_Common_Neighbor_num×÷Îªindex½«ËüÃÇÒ»ÌõÌõÕÒ³öÀ´ 
					{														  //²¢°ÑÑ¡ÖÐ±ßÖÐ¶È×î´óµÄÕÒ³öÀ´ 
						 
						int j = Max_Common_Neighbor_j_Point[k];
						if(Min_Edge > Clique[Max_i][j].Edge_Delete)                //ÕÒ³öÉ¾³ý±ß×îÉÙ±ßµÄÁ½¸öµã 
						{
							Min_Edge = Clique[Max_i][j].Edge_Delete;
							Max_Common_Neighbor_j_Point_Last = j;
						}
						
					}
																					//ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄedge(i,j) 
					Max_j =  Max_Common_Neighbor_j_Point_Last; 
				} 
				else															//×î´óCommon_NeighborµÄ±ßÖ»ÓÐÒ»Ìõ 
				{
																				 //ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄµÄedge(i,j) 
					Max_j = Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num]; //Max_Common_Neighbor_num¾ÍÊÇindex 
				} 
				{
					//ÖØÐÂ»ñµÃ Max_i ºÍ Max_j Á½¸ö½ÚµãÎª×îÓÐÑ¡Ôñµã 
					//Max_i;
					//Max_j;
					goto Step2_1; 
				} 
			}			
	}//end while(Max_Degree_Increasing_Order)
	
	/*¼ÆËãCliqueµÄ¸öÊý*/
	cout << "******************" << endl;
	for(int i = 1; i <= n; i++)
	{
		if(NodeList[i][1] != 0)					//Clique±£´æÔÚNodeList[][]ÖÐ NodeList[i][1] = 1±íÊ¾ÕâÀïÓÐÒ»¸öÍÅ
												//NodeList[i][1] = 0±íÊ¾ÕâÀïÃ»ÓÐÍÅ 
		{
			Clique_Count++;	
		} 
	} 
	cout << "print Clique_Count = " << Clique_Count << endl; 
	for(int i = 1; i <= n; i++)
	{
		if(NodeList[i][1] != 0)									//±£Ö¤ÕâµãµÄ¸ù½ÚµãÒ»¶¨´æÔÚ~ 
		{
			cout << "Clique[" << i << "]:( " << i << ",";		//ÔÚ¼ì²éËüÆäÖÐ»¹°üº¬ÄÄÐ©½Úµã 
			for(int j = i + 1; j <= n; j++)
			{
				if(NodeList[i][j] != 0)
				{
					cout << j << ",";
				}	
			}
			cout << ")" << endl;
		}

	}
	finish = clock();
	
	cout <<"**********************" << endl;
	cout << "Edge_Delete Time = " << (finish - start )/CLOCKS_PER_SEC << "s" << endl;
	cout <<"**********************" << endl;
	/***********************************************************************/
	
	
	for(int i = 1; i <= n; i++)							//°ÑClique[i][j].EdgeListµÄ±¸·Ýµ½Clique[i][j].EdgeList_New 
	{													//±¸·ÝÊý¾Ý 
		Node[i] = Node_New[i];
		for(int j = 1; j <= n; j++)
		{
			Clique[i][j].EdgeList = Clique[i][j].EdgeList_New;
			NodeList[i][j]  = NodeList_New[i][j];
		}
	}
	max_Degree_Inceasing_Order = 1;					//ÖØÐÂÀ´Ò»´Î 
	Clique_Count = 0;
	
	start = clock();
end2:
	
	while(max_Degree_Inceasing_Order)					// max_Degree_Inceasing_Order = 0 ×÷Îª³ÌÐòÍ£Ö¹µÄ±êÖ¾£¬
														// max_Degree_Inceasing_Order ½Úµã¶ÈÅÅÐòºóµÄ×î´óÖµ ×î´óÖµÎª0 ±íÃ÷Ã¿¸ö½Úµã²»ÏàÁ¬£¬
														//ÔòÈ«²¿µãÒÑ¾­È«²¿·Öµ½¸÷¸öClique 
	{
		
Step1_2:
		for(int i =1; i <= n; i++)						//Ã¿´Î¶¼°Ñ ×î´óCommon_NeighborÅÅÐòÊý×éÖÃÁã 
		{
			Common_Neighbor_Sort[i] = 0;	
		} 
	
		Max_Degree = 0;                                //Îª·ÀÖ¹ÉÏ´ÎÁ½¸ö½Úµã¶ÈµÄÓ°Ïì£¬×î´ó¶ÈÃ¿´Î¶¼µÃ¸üÐÂ 
		 
																// Í³¼ÆÃ¿¸ö½ÚµãµÄ¶È±£´æµ½Degree[],Êý×éÏÂ±í¼´Îª½ÚµãµÄ±êºÅ									
		for(int i = 1; i <= n; i++)
		{
			Degree[i] = 0;										//Ã¿¸ö½ÚµãµÄ¶È³õÊ¼»¯Îª0 
			for(int j = 1; j <= n; j++)
			{
				Degree[i] = Degree[i] + Clique[i][j].EdgeList; // Ã¿Ò»ÐÐµÄÖµµÄ×ÜºÍ¼´ÎªÄ³¸ö½ÚµãµÄ¶È 
			}	
			Degree_Inceasing_Order[i] = Degree[i];				//½«Degree[]µÄÖµÒÀ´Î´æÈëDegree_Increasing_Order[]ÓÃÓÚÅÅÐò
																//ÒÀ¾ÉÒª±£´æDegree²»±ä£¬·½±ã ¡°²éÑ¯Ê±½Úµã¡± Ê±Ê¹ÓÃ 
		} 
									
		SelectSort(Degree_Inceasing_Order, n);					//½«½ÚµãµÄ¶È½øÐÐÅÅÐò~ 
		
		max_Degree_Inceasing_Order = Degree_Inceasing_Order[1];

		if(max_Degree_Inceasing_Order == 0)						//ÒÔ»ñÈ¡×î´ó½Úµã¶ÈÎª0£¬ÂíÉÏÖÕÖ¹³ÌÐò 
		{
			goto end2;
		} 
	
		/*¼ÆËãÃ¿Ìõ±ßµÄcommon neighborÊýÁ¿*/
		for(int i = 1; i <= n; i++)				
		{
			
			for(int j = 1; j <= n; j++)						//¿ØÖÆÐÐµÄ±ä»¯ 
			{
				First[j] = Clique[i][j].EdgeList;           //  ÌáÈ¡µÚiÐÐÔªËØ 
			
			}	
			
			for(int k = 1; k <= n; k++)						//¿ØÖÆÁÐµÄ±ä»¯
			{
			
				if(Clique[i][k].EdgeList == 1)				//±£Ö¤²Ù×÷µÄÁ½¸öµãÊÇÏàÁ¬µÄ 
				{
				
					for(int j = 1; j <= n; j++)			 
					{
						Second[j] = Clique[k][j].EdgeList;  //  ÌáÈ¡µÚkÐÐÔªËØ 
					}
				
					int Diff = 0;								//ÁÚ¾Ó¼ÆÊý 	
					for(int u = 1; u <= n; u++)
					{
						if(First[u] == Second[u] && First[u] != 0)			//ÏàÁ¬µÄÁ½¸öµã(edge) ÓÐ¹²Í¬µÄµã£¨Common_Neignbor£©,²¢ÇÒ0²»ËãÏàÁ¬ 
						{
								Diff = Diff + 1;
						}	
					}	
					Clique[i][k].Common_Neighbor = Diff;    //Ã¿Ìõ±ßµÄCommon_NeighborÊýÁ¿ 
				}
				else
					Clique[i][k].Common_Neighbor = 0;	
			}
		} 

		for(int i = 1; i <= n; i++)				//	Ö»»ñÈ¡Common_NeighborÉÏÈý½Ç²¿·ÖÊý¾Ý£¬±£Ö¤Common_Neighbor[][]Ö»±£´æ²»Í¬±ßµÄ¸öÊý 
		{
			for(int j = 1; j <= n; j++)
			{		
				if(i <= j)
				{
					Clique[i][j].Common_Neighbor_New = Clique[i][j].Common_Neighbor; //½«Common_NeighborµÄÉÏÈý½ÇÌáÈ¡³öÀ´ 
				} 
				if(j == n)
				{	
				} 	
			}	
		} 

		/*******************************************************/
		/***********Common_Neighbor_Sort³öÁËÎÊÌâ****************/
		/*******************************************************/
		/*½«Ã¿Ò»¸ö½Úµã¶ÔÓ¦µÄ×î´óCommon_NeighborÕÒ³öÀ´*/
		for(int i = 1, j = 1; i <= n; i++)
		{														//*********************Ö®Ç°ÕâÀïºÃÏñ´íÁË***************************// 
			int max = Clique[i][i].Common_Neighbor_New;         //´Ó¶Ô½ÇÏß¿ªÊ¼  ~~~~~~~~~~~~²ÅÊÇÕýÈ·µÄ  Õâ¸öÖµµÈÓÚ0  ²»È»»á³öÏÖËæ»úÖµ 
			for(j = i; j <= n; j++)
			{
				if(max < Clique[i][j].Common_Neighbor_New)
				{ 
					max = Clique[i][j].Common_Neighbor_New;	//Èôµ±Ç°maxÖµ±È Clique.Common_Neighbor_New[i][j]Ð¡£¬ÔòÌæ»» maxÖµ 
				}
			}
			Common_Neighbor_Sort[i] = max;
		}
			
		SelectSort(Common_Neighbor_Sort, n);			//¶ÔÍ³¼Æ³öÀ´µÄÃ¿¸öµãµÄ×î´óCommon_NeighborÊýÁ¿½øÐÐÅÅÐò 
	
		/*Ê×ÏÈÕÒ³öCommon_Neighbor×î´óµÄ£¬ÈçCommon_Neighbor×î´óÖµÎ¨Ò»£¬Ôò¼ÌÐø£¬Èç×î´óÖµ²»Î¨Ò»ÔòÔÙ±È½Ï
		Degree[],ÓÐÏÞºÏ²¢¶È×î´óµÄÁ½¸ö½Úµã*/

		int Max_Common_Neighbor_num = 0; 					//Í³¼ÆÓÐÓÃ×î´óCommon_NeighborµÄ±ßµÄÊýÁ¿ 
		int Max_Common_Neighbor_i_Point[n];					//±£´æÃ¿Ìõ±ßµÄi½Úµã 
		int Max_Common_Neighbor_j_Point[n];					//±£´æÃ¿Ìõ±ßµÄj½Úµã 
		int Max_Common_Neighbor_i_Point_Last;				//µ±×î´óCommon_NeighborµÄ±ß²»Ö¹Ò»ÌõÊ±£¬ÐèÒªÕÒ¶È×î´óµÄÄÇÁ½¸ö½Úµã »ñÈ¡i½Úµã 
		int Max_Common_Neighbor_j_Point_Last;				//»ñÈ¡j½Úµã 
		int Max_i;											//×îÓÅµÄÁ½¸öµã~µÄ ±êºÅ 
		int Max_j;	
		Max_Common_Neighbor_num = 0;										//Ò»¶¨´æÔÚ Max_j > Max_i 
		
		for(int i = 1; i <= n; i++)
		{
			for(int j = i + 1; j <= n; j++)
			{
				// Common_NeighborÊýÁ¿×î´óµãÎª Common_Neighbor_Sort[1]  Ã¿´Î¶¼Ö»ÄÃ×î´óµÄ³öÀ´±È½Ï¼´¿É  
				if(Common_Neighbor_Sort[1] == Clique[i][j].Common_Neighbor_New && Clique[i][j].EdgeList != 0)	
				//ÕÒµ½×î´óCommon_NeighborµÄÁ½¸ö½Úµã ·ÀÖ¹×î´óCommon_NeighborÎª0Ê±³öÏÖ´íÎó£¬±£Ö¤Ñ¡ÖÐµÄÁ½¸ö½Úµã±ØÐëÏàÁ¬ 
				{
					Max_Common_Neighbor_num++;					 						//Í³¼Æ×î´óCommon_NeighborÊýÁ¿ 
					Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num] = i;			//Í³¼Æ×î´óCommon_NeighborÎ»ÖÃ ¼´£ºÁ½¸ö½Úµã±êºÅ 
					Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num] = j;			//Max_Common_Neighbor_num¿ÉÒÔ×÷Îªindex 
				}
			}	
		} 

		Max_Degree = 0;
		if(Max_Common_Neighbor_num != 1)								//º¬ÓÐ×î´óCommon_NeighborµÄ±ß²»Ö¹Ò»Ìõ 
		{
			for(int k = Max_Common_Neighbor_num; k >= 1; k-- )		  //Í¨¹ýMax_Common_Neighbor_num×÷Îªindex½«ËüÃÇÒ»ÌõÌõÕÒ³öÀ´ 
			{														  //²¢°ÑÑ¡ÖÐ±ßÖÐ¶È×î´óµÄÕÒ³öÀ´ 
				int i = Max_Common_Neighbor_i_Point[k]; 
				int j = Max_Common_Neighbor_j_Point[k];
				if(Max_Degree < (Degree[i] + Degree[j]))				//ÕÒ³ö¶È×î´óµÄÁ½¸öµã 
				{
					Max_Degree = Degree[i] + Degree[j];
					Max_Common_Neighbor_i_Point_Last = i;				//ÒÑ¾­ÕÒ³ö¶È×î´óµÄÁ½¸öµã 
					Max_Common_Neighbor_j_Point_Last = j;
				}
			}
			Max_i =  Max_Common_Neighbor_i_Point_Last;					//ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄedge(i,j) 
			Max_j =  Max_Common_Neighbor_j_Point_Last; 
		} 
		else															//×î´óCommon_NeighborµÄ±ßÖ»ÓÐÒ»Ìõ 
		{
			Max_i = Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num]; //ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄµÄedge(i,j) 
			Max_j = Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num]; //Max_Common_Neighbor_num¾ÍÊÇindex 
		} //end Step1
Step2_2:
		{  
			//¶ÔMax_i ºÍMax_j ½øÐÐ´¦Àí ¾ÍÊÇ¶ÔClique·ÖÍÅ½øÐÐ´¦Àí£¬Node[],NodeList[][]¶¼Òª½øÐÐ´¦Àí
			//Madx_i ºÍMax_j ±íÊ¾×î´óCommon_Neighbor ²¢ÓÐ×î´ó¶ÈµÄÁ½¸öÁ¬½Óµã edge(Max_i,Max_j)
			//Node[] == 1Ê±±íÊ¾Õâ¸öµãÎ´ÊÜµ½´¦Àí£¬Node[] == 0Ê±±íÊ¾ÒÑ¾­¼ÓÈëÄ³¸öClique
			//NodeList[i][1] == 1Ê±±íÊ¾ÕâÀïÓÐÒ»¸öClique NodeList[i][1] == 0Ê±±íÊ¾ÕâÀï²»´æÔÚClique  
			
			//Clique[Max_i][Max_j].EdgeList ÐèÒª±»´¦Àí 
			//´æÔÚÓÚClique[Max_i][]µ«²»´æÔÚÓëClique[Max_j][]ÖÐµÄµã¾ùÎª0 
			//Clique[Max_j][].EdgeListÈ«²¿Îª0
			
			//ÒÑ¾­µÃµ½ Max_i  Max_j Ä¿Ç°½ö¶ÔËüÃÇÁ½¸öµã½øÐÐ²Ù×÷  ************************ 
			 
			
			//¶Ô¼ÓÈëCLique½øÐÐ´¦Àí  Ò»¶¨´æÔÚ Max_i < Max_j  
	
			int temp;
			if(Max_i > Max_j)										//ÈôMax_i½Ï´ó£¬Ôò»¥»»Max_iÓëMax_jµÄÖµ 
			{
				temp  = Max_j;
				Max_j = Max_i;
				Max_i = temp; 
			}
					
			NodeList[Max_j][1] = 0;							     //¼õÉÙÒ»¸öCLique
			Node[Max_j]		   = 0;					  	      	//¼õÉÙÒ»¸öNode ¾ù±íÊ¾½«Max_jÓëMax_iºÏ²¢ÎªMax_i 
			
																//±£´æÍ¬ÔÚÒ»¸öÍÅÀïÃæ  ¿¼ÂÇÒ»¸öÎÊÌâ~  
																//¾ÍÊÇµ±Ô­À´µÄMax_i > Max_j Ê±Òª°Ñ Max_i Óë Max_j»¥»»
																//NodeList[Max_j][i]µÄÖµÒ²µÃ±£´æµÄÒª±£´æµ½NodeList[Max_i][i]  
			{
				NodeList[Max_i][Max_j] = Max_j;					//Ö÷ÒªÊÇNodeList[Max_j][1] = Max_j 
				for(int i = 2; i <= n; i++)
				{
					if(NodeList[Max_j][i] != 0)					//½«ÊôÓÚNodeList[Max_j][i]¹é²¢µ½NodeList[Max_i][i]ÖÐ 
					{
						NodeList[Max_i][i] = i;
					}	
				}
			}		
			for(int i = 1; i <= n; i++)								//NodeList[Max_j][i]ÖÐµÄµãÒÑ¾­±»¹é²¢µ½NodeList[Max_i][i]ÁË£¬½«Nodelist[Max_j][i]ÇåÁã 
			{
				NodeList[Max_j][i] = 0;	
			}											
	
Step3_2:
			for(int j = 1; j <= n; j++)					     	//¿ØÖÆÐÐµÄ±ä»¯ 
			{
				First[j] = Clique[Max_i][j].EdgeList;         //  ÌáÈ¡µÚiÐÐÔªËØ 
				Second[j] = Clique[Max_j][j].EdgeList;       //  ÌáÈ¡µÚkÐÐÔªËØ 
			}	
			for(int u = 1; u <= n; u++)
			{												//ÒÑ¾­Ã÷È·Max_iºÍMax_jÊÇÏàÁ¬µÄ£¬²é¿´ËüÃÇ¶ÔÓ¦ÁÚ½Ó¾ØÕóµÄMax_iÐÐºÍMax_jÐÐ
															//¶ÔÓ¦ÁÐÊÇ·ñÏàµÈ£¬ÏàµÈÇÒµÈÓÚ1±íÊ¾µÚÈý¸öµãkÓëMax_i¡¢Max_jÏàÁ¬
															//ÔòEdge(Max_i,k)(Èç¹ûk>Max_iÊ± ÔòÎªEdge(k, Max_i))²»ÐèÒªÉ¾³ý£¬·´Ö®ÐèÒªÉ¾³ý 
				if(First[u] != Second[u] && First[u] == 1)	//´æÔÚÒ»¸öµã½öÓëÏàÁ¬µÄMax_iµãÏàÁ¬ ¼´ Clique[Max_i][u].EdgeList = 1;
				{
						Clique[Max_i][u].EdgeList = 0;		//Éú³ÉµÄÊÇÎÞÏòÍ¼£¬ÐèÒªÖÃ¶Ô³ÆµÄÁ½¸öÖµÎª0£¬¼´ÎªÉ¾³ý±ß 
						Clique[u][Max_i].EdgeList = 0;
				}			
			}
			// ½«Óë±êºÅ´óµÄµã¼´Max_jÏàÁ¬µÄ±ßÈ«²¿É¾µô	//ÕâÑù×öÉÙÁËÒ»Ð©¹¤×÷£¬±È½ÏºÃÀí½â£¬¿ÉÒÔÖ±½ÓËµ²»Í¨ 
			for(int i = 1; i <= n; i++)
			{
				Clique[Max_j][i].EdgeList = 0;			//Éú³ÉµÄÊÇÎÞÏòÍ¼£¬ÐèÒªÖÃ¶Ô³ÆµÄÁ½¸öÖµÎª0£¬¼´ÎªÉ¾³ý±ß 
				Clique[i][Max_j].EdgeList = 0;
			}
			
Step4_2:
			Max_i;									 	//Max_i ºÍ Max_j ºÏ²¢Îª Max_i 
		} 
	
Step5_2:
		/*ÓÉÓÚ½Úµã±»ÐÞ¸Ä£¬Ã¿¸ö½ÚµãµÄ¶ÈÒ²±»ÐÞ¸ÄÁË ÖØÐÂ¼ÆËã¶ÈµÄÖµ*/ 
			for(int i = 1; i <= n; i++)
			{
				Degree[i] = 0;										//Ã¿¸ö½ÚµãµÄ¶È³õÊ¼»¯Îª0 
				for(int j = 1; j <= n; j++)
				{
					Degree[i] = Degree[i] + Clique[i][j].EdgeList; // Ã¿Ò»ÐÐµÄÖµµÄ×ÜºÍ¼´ÎªÄ³¸ö½ÚµãµÄ¶È 
				}	
				Degree_Inceasing_Order[i] = Degree[i];				//½«Degree[]µÄÖµÒÀ´Î´æÈëDegree_Increasing_Order[]ÓÃÓÚÅÅÐò
																	//ÒÀ¾ÉÒª±£´æDegree²»±ä£¬·½±ã ¡°²éÑ¯Ê±½Úµã¡± Ê±Ê¹ÓÃ 
			} 
			/*´òÓ¡Ã¿¸ö½ÚµãµÄ¶È*/
										//½«½ÚµãµÄ¶È½øÐÐÅÅÐò~ 
			SelectSort(Degree_Inceasing_Order, n);
			
			max_Degree_Inceasing_Order = Degree_Inceasing_Order[1];

			if(max_Degree_Inceasing_Order == 0)						//ÒÔ»ñÈ¡×î´ó½Úµã¶ÈÎª0£¬ÂíÉÏÖÕÖ¹³ÌÐò 
			{
				goto end2;
			}  	

			if(Degree[Max_i] == 0)					//Èç¹ûMax_i½Úµã¶ÀÁ¢ÁË£¬ÁíÑ¡Ò»Ìõ±ß¼´ÁíÍâÁ½¸öµã 
			{
				goto Step1_2;
			}
			else								    // »¹ÓÐÓëMax_iÏàÁ¬µÄ±ß 
			{
				/*¼ÆËã°üº¬Max_i½ÚµãµÄ±ßµÄCommon_NeighborµÄ×î´óÖµÇé¿ö*/	
				for(int j = 1; j <= n; j++)						//¿ØÖÆÐÐµÄ±ä»¯ 
				{
					First[j] = Clique[Max_i][j].EdgeList;           //  ÌáÈ¡µÚiÐÐÔªËØ 
				}	
				for(int k = 1; k <= n; k++)						//¿ØÖÆÁÐµÄ±ä»¯
				{
					if(Clique[Max_i][k].EdgeList == 1)				//±£Ö¤²Ù×÷µÄÁ½¸öµãÊÇÏàÁ¬µÄ 
					{
						for(int j = 1; j <= n; j++)			 
						{
							Second[j] = Clique[k][j].EdgeList;  //  ÌáÈ¡µÚkÐÐÔªËØ 
						}
						int Diff = 0;								//ÁÚ¾Ó¼ÆÊý 	
						for(int u = 1; u <= n; u++)
						{
							if(First[u] == Second[u] && First[u] != 0)			//ÏàÁ¬µÄÁ½¸öµã ÓÐ¹²Í¬µÄµã£¨Common_Neignbor£©,²¢ÇÒ0²»ËãÏàÁ¬ 
							{
									Diff = Diff + 1;
							}	
						}	
						Clique[Max_i][k].Common_Neighbor = Diff;    //Ã¿Ìõ±ßµÄCommon_NeighborÊýÁ¿ 
					}
					else
						Clique[Max_i][k].Common_Neighbor = 0;	
				}
				//	Ö»»ñÈ¡Common_NeighborÉÏÈý½Ç²¿·ÖÊý¾Ý£¬±£Ö¤Common_Neighbor[][]Ö»±£´æ²»Í¬±ßµÄ¸öÊý 
				for(int j = 1; j <= n; j++)						//²»ÖªµÀMax_i ºÍ jË­´óË­Ð¡ 
				{
					Clique[Max_i][j].Common_Neighbor_New = Clique[Max_i][j].Common_Neighbor; //½«Common_NeighborµÄÉÏÈý½ÇÌáÈ¡³öÀ´ 
				}	
	
				//ÒÑ¾­»ñµÃ Clique[Max_i][k].Common_Neighbor_New	
				int max = Clique[Max_i][1].Common_Neighbor_New; 
				for(int j = 2; j <= n; j++)
				{
					if(max < Clique[Max_i][j].Common_Neighbor_New)
					{ 
						max = Clique[Max_i][j].Common_Neighbor_New;	//Èôµ±Ç°maxÖµ±È Clique.Common_Neighbor_New[i][j]Ð¡£¬ÔòÌæ»» maxÖµ 
					}
				}
				Common_Neighbor_Sort[1] = max;
				// Max_i×î´óµÄCommon_Neighbor Îª max 
				//×î´óµÄCommon_Neighbor = max
				//Á½¸ö¶¥µã·Ö±ðÎª Max_i Max_j ÅÐ¶Ïmax ÊÇ·ñÎ¨Ò»
				Max_Common_Neighbor_num = 0;
				for(int j = 1; j <= n; j++)
				{
					// Common_NeighborÊýÁ¿×î´óµãÎª Common_Neighbor_Sort[1]  Ã¿´Î¶¼Ö»ÄÃ×î´óµÄ³öÀ´±È½Ï¼´¿É  
					if(Common_Neighbor_Sort[1] == Clique[Max_i][j].Common_Neighbor_New && Clique[Max_i][j].EdgeList != 0)	
					//ÕÒµ½×î´óCommon_NeighborµÄÁ½¸ö½Úµã ·ÀÖ¹×î´óCommon_NeighborÎª0Ê±³öÏÖ´íÎó£¬±£Ö¤Ñ¡ÖÐµÄÁ½¸ö½Úµã±ØÐëÏàÁ¬ 
					{
						Max_Common_Neighbor_num++;					 						//Í³¼Æ×î´óCommon_NeighborÊýÁ¿ 
						//Max_Common_Neighbor_i_Point[Max_Common_Neighbor_num] = Max_i;			//Í³¼Æ×î´óCommon_NeighborÎ»ÖÃ ¼´£ºÁ½¸ö½Úµã±êºÅ 
						Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num] = j;			//Max_Common_Neighbor_num¿ÉÒÔ×÷Îªindex 
					}
				}	
				Max_Degree = 0;
				if(Max_Common_Neighbor_num != 1)								//º¬ÓÐ×î´óCommon_NeighborµÄ±ß²»Ö¹Ò»Ìõ 
				{
					for(int k = Max_Common_Neighbor_num; k >= 1; k-- )		  //Í¨¹ýMax_Common_Neighbor_num×÷Îªindex½«ËüÃÇÒ»ÌõÌõÕÒ³öÀ´ 
					{														  //²¢°ÑÑ¡ÖÐ±ßÖÐ¶È×î´óµÄÕÒ³öÀ´ 
						 
						int j = Max_Common_Neighbor_j_Point[k];
						if(Max_Degree < (Degree[Max_i] + Degree[j]))				//ÕÒ³ö¶È×î´óµÄÁ½¸öµã 
						{
							Max_Degree = Degree[Max_i] + Degree[j];
																					//ÒÑ¾­ÕÒ³ö¶È×î´óµÄÁ½¸öµã 
							Max_Common_Neighbor_j_Point_Last = j;
						}
					}
																					//ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄedge(i,j) 
					Max_j =  Max_Common_Neighbor_j_Point_Last; 
				} 
				else															//×î´óCommon_NeighborµÄ±ßÖ»ÓÐÒ»Ìõ 
				{
																				 //ÒÑ¾­ÕÒµ½×î´óCommon_Neighborµã¼°×î´ó¶ÈµÄµÄedge(i,j) 
					Max_j = Max_Common_Neighbor_j_Point[Max_Common_Neighbor_num]; //Max_Common_Neighbor_num¾ÍÊÇindex 
				} 
				{
					//ÖØÐÂ»ñµÃ Max_i ºÍ Max_j Á½¸ö½ÚµãÎª×îÓÐÑ¡Ôñµã 
					//Max_i;
					//Max_j;
					goto Step2_2; 
				} 
			}			
	}//end while(Max_Degree_Increasing_Order)
	
	//#ifdef Debug 
		/*¼ÆËãCliqueµÄ¸öÊý*/
		cout << "******************" << endl;
		for(int i = 1; i <= n; i++)
		{
			if(NodeList[i][1] != 0)					//Clique±£´æÔÚNodeList[][]ÖÐ NodeList[i][1] = 1±íÊ¾ÕâÀïÓÐÒ»¸öÍÅ
													//NodeList[i][1] = 0±íÊ¾ÕâÀïÃ»ÓÐÍÅ 
			{
				Clique_Count++;	
			} 
		} 
		cout << "print Clique_Count = " << Clique_Count << endl; 
		for(int i = 1; i <= n; i++)
		{
			if(NodeList[i][1] != 0)									//±£Ö¤ÕâµãµÄ¸ù½ÚµãÒ»¶¨´æÔÚ~ 
			{
				cout << "Clique[" << i << "]:( " << i << ",";		//ÔÚ¼ì²éËüÆäÖÐ»¹°üº¬ÄÄÐ©½Úµã 
				for(int j = i + 1; j <= n; j++)
				{
					if(NodeList[i][j] != 0)
					{
						cout << j << ",";
					}	
				}
				cout << ")" << endl;
			}
		}
	
	finish = clock();
	
	cout <<"**********************" << endl;
	cout << "Degree_Delete Time = " << (finish - start )/CLOCKS_PER_SEC<< "s" << endl;
	cout <<"**********************" << endl; 
	//#endif 

	cout << "Do you want to continue? ¡¾1¡¿ Yes ¡¾2¡¿ No" << endl;
	int flag_go_on;
	cin >> flag_go_on;
	if(flag_go_on == 1)
	{
		goto go_on;
	}
	return 0;
}

int SelectSort(int *A, int n)				//¶¨ÒåÒ»¸öÅÅÐòº¯Êý
{
	int temp;
	for(int i = 1; i < n ; i++)
	{
		int max = i;
		for(int j = i + 1; j <= n; j++)
		{
			if(A[max] < A[j])
			{
				max = j;
			}		
		}
		{
			temp = A[max];
			A[max] = A[i];
			A[i]   = temp;
		}
	} 
	return 0;
}
