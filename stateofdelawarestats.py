import pandas as pd
import numpy as np

student_assessment_df = pd.read_csv('Student_Assessment_Performance.csv')

student_assessment_df = student_assessment_df[student_assessment_df['Race'] == 'All Students']
student_assessment_df = student_assessment_df[student_assessment_df['Gender'] == 'All Students']
student_assessment_df = student_assessment_df[student_assessment_df['SpecialDemo'] == 'All Students']
student_assessment_df = student_assessment_df[student_assessment_df['RowStatus'] == 'REPORTED']
student_assessment_df = student_assessment_df[student_assessment_df['Grade'] == 'All Students']

student_assessment_df = student_assessment_df.drop(columns=['Race', 'Gender', 'SpecialDemo', 'RowStatus', 'SubGroup', 'Geography', \
    'ScaleScoreAvg','Tested','Proficient'])

student_enrollment_df = pd.read_csv('Student_Enrollment.csv')

student_enrollment_df = student_enrollment_df[student_enrollment_df['Race'] == 'All Students']
student_enrollment_df = student_enrollment_df[student_enrollment_df['Gender'] == 'All Students']
student_enrollment_df = student_enrollment_df[student_enrollment_df['SpecialDemo'] == 'All Students']
student_enrollment_df = student_enrollment_df[student_enrollment_df['Grade'] == 'All Students']

student_enrollment_df = student_enrollment_df.drop(columns=['Race', 'Gender', 'SpecialDemo', 'RowStatus', 'SubGroup', 'Geography','EOYEnrollment', \
    'PctOfEOYEnrollment', 'Grade','Students'])

merged_df = student_assessment_df.merge(student_enrollment_df, on=['School Year', 'District Code', 'District','School Code', 'Organization'], how='inner')
merged_df['FallEnrollment'] = merged_df['FallEnrollment'].astype(float)
merged_df = merged_df[merged_df['Organization'].str.contains("State of Delaware")==True]

del student_assessment_df
del student_enrollment_df

merged_df = merged_df.drop(columns=['District Code', 'District'])

educator_df = pd.read_csv('Educator_Average_Salary.csv')

educator_df = educator_df[educator_df['Race'] == 'All Educators']
educator_df = educator_df[educator_df['Gender'] == 'All Educators']
educator_df = educator_df[educator_df['SpecialDemo'] == 'All Educators']
educator_df = educator_df[educator_df['Experience'] == 'ALL']
educator_df = educator_df[educator_df['Organization'].str.contains("State of Delaware")==True]

educator_df = educator_df[['School Year', 'School Code', 'Organization', 'Job Classification', 'Educators (FTE)']]
educator_df = educator_df[educator_df['Job Classification'] != 'ALL']
listofjobs = educator_df['Job Classification'].unique()

educator_df = pd.pivot(educator_df, index=['School Year', 'School Code', 'Organization'], columns='Job Classification', values='Educators (FTE)')
educator_df = educator_df.reset_index()

educator_df['Teacher, Regular Elementary'] = educator_df['Teacher, Regular Elementary'].fillna(0)
educator_df['Teacher, Special Elementary'] = educator_df['Teacher, Special Elementary'].fillna(0)
educator_df['Teacher, Regular Secondary'] = educator_df['Teacher, Regular Secondary'].fillna(0)
educator_df['Teacher, Special Secondary'] = educator_df['Teacher, Special Secondary'].fillna(0)

educator_df['Teacher, Regular'] = educator_df['Teacher, Regular Elementary'] + educator_df['Teacher, Regular Secondary']
educator_df['Teacher, Special'] = educator_df['Teacher, Special Elementary'] + educator_df['Teacher, Special Secondary']

educator_df.drop(columns=['Teacher, Regular Elementary','Teacher, Special Elementary','Teacher, Regular Secondary','Teacher, Special Secondary'], axis=1)

df = merged_df.merge(educator_df, on=['School Year', 'School Code', 'Organization'], how='inner')

del educator_df
del merged_df

df['Students Per Teacher, Regular'] = df['FallEnrollment'] / df['Teacher, Regular']
df['Students Per Teacher, Special'] = df['FallEnrollment'] / df['Teacher, Special']
df = df.drop(['Teacher, Regular','Teacher, Special'], axis=1)

for item in listofjobs:
    df['Students Per ' + str(item)] = df['FallEnrollment'] / df[item]
    df = df.drop(item, axis=1)

df = df.drop(['Students Per Teacher, Regular Elementary','Students Per Teacher, Special Elementary','Students Per Teacher, Regular Secondary',\
    'Students Per Teacher, Special Secondary'], axis=1)

df = df.replace([np.inf, -np.inf], np.nan)

df = df[df['Assessment Name'] == 'Smarter Balanced Summative Assessment']
df = df[df['School Year'] == 2022] 

df.to_csv('StateofDelawarestats.csv', index=False)